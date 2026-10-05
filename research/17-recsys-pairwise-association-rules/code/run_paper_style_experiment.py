"""Evaluation following the protocol of Section 4 of Osadchiy et al. (2019), on synthetic meals.

Protocol (paper): meals with >= 2 foods; k-fold cross validation; from each test meal sample k input foods
(k = 1..5) and keep the remaining foods (at least one) as the 'omitted' foods; each model returns its top 15;
report precision, recall and nDCG@15, plus training and recommendation time.
Differences from the paper (documented): synthetic data; 5 folds instead of 10; AR mines itemsets up to size 4
(antecedent <= 3) instead of unbounded FP-growth; nDCG uses the usual ideal ranking (paper fixes IDCG = 1);
recall = correct predictions / number of omitted foods of the meal.
"""
import os, time, json, csv
import numpy as np
from synthetic_meals import generate
from paper_algorithms import PARMatrix, TICSparse, AR

OUT = os.path.join(os.path.dirname(__file__), "..", "results"); os.makedirs(OUT, exist_ok=True)
N_MEALS, FOLDS, Q_PER_K, TOPN = 20000, 5, 300, 15
MIN_COUNT = 6          # = 3e-4 * 20000, the (corrected) threshold used for AR in the paper
rng = np.random.default_rng(11)
X, foods = generate(N_MEALS, seed=3)
n_foods = len(foods)
perm = rng.permutation(N_MEALS); folds = np.array_split(perm, FOLDS)
disc = 1.0 / np.log2(np.arange(2, TOPN + 2))


class Popularity:
    def fit(self, X): self.p = X.sum(0).astype(float); return self
    def recommend(self, IF, k=TOPN):
        s = self.p.copy(); s[list(IF)] = -1; top = np.argsort(-s)[:k]; return [int(i) for i in top]


def as_ids(rec):
    return [r[0] if isinstance(r, tuple) else r for r in rec]


def metrics(rec, held):
    held = set(held); rec = as_ids(rec)[:TOPN]
    hit = [1 if r in held else 0 for r in rec]
    tp = sum(hit)
    dcg = sum(h * d for h, d in zip(hit, disc))
    idcg = disc[:min(len(held), TOPN)].sum()
    return tp / max(len(rec), 1), tp / len(held), dcg / idcg


models = {"Popularity": lambda: Popularity(), "AR": None, "TIC": lambda: TICSparse(), "PAR": lambda: PARMatrix()}
res = {m: {k: [] for k in range(1, 6)} for m in models}
times = {m: {"train": [], "rec": []} for m in models}

for fi in range(FOLDS):
    test_idx = folds[fi]; train = X[np.concatenate([folds[j] for j in range(FOLDS) if j != fi])]
    fitted = {}
    for name in models:
        t = time.perf_counter()
        if name == "AR":
            meals = [set(np.flatnonzero(r).tolist()) for r in train]
            fitted[name] = AR().fit(meals, min_count=MIN_COUNT, max_len=4)
        else:
            fitted[name] = models[name]().fit(train)
        times[name]["train"].append(time.perf_counter() - t)
    print(f"fold {fi}: trained; AR rules = {len(fitted['AR'].rules)}", flush=True)
    for k in range(1, 6):
        cases = []
        while len(cases) < Q_PER_K:
            items = np.flatnonzero(X[rng.choice(test_idx)])
            if len(items) < k + 1: continue
            IF = rng.choice(items, size=k, replace=False)
            cases.append((IF.tolist(), [i for i in items if i not in set(IF.tolist())]))
        for name, mdl in fitted.items():
            for IF, held in cases:
                t = time.perf_counter(); rec = mdl.recommend(set(IF) if name == "AR" else IF, TOPN) if name != "Popularity" else mdl.recommend(IF)
                times[name]["rec"].append(time.perf_counter() - t)
                res[name][k].append(metrics(rec, held))

rows = []
for name in models:
    for k in range(1, 6):
        a = np.array(res[name][k]); p, r, n = a.mean(0)
        rows.append(dict(model=name, input_size=k, precision=round(float(p), 4), recall=round(float(r), 4), ndcg15=round(float(n), 4), n_queries=len(a)))
with open(os.path.join(OUT, "paper_style_results.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
tt = {m: dict(train_s=round(float(np.mean(v["train"])), 3), mean_recommend_ms=round(1000 * float(np.mean(v["rec"])), 3)) for m, v in times.items()}
json.dump(dict(n_meals=N_MEALS, folds=FOLDS, queries_per_k_per_fold=Q_PER_K, n_foods=n_foods, mean_meal_size=float(X.sum(1).mean()),
               ar_min_count=MIN_COUNT, ar_rules_last_fold=len(fitted["AR"].rules), timing=tt), open(os.path.join(OUT, "paper_style_summary.json"), "w"), indent=2)
for r in rows: print(r)
print(json.dumps(tt, indent=1))

# paired comparison on identical queries (PAR minus other), all input sizes pooled
pair = {}
for other in ("AR", "TIC", "Popularity"):
    d = []
    for k in range(1, 6):
        a = np.array(res["PAR"][k])[:, 2]; b = np.array(res[other][k])[:, 2]; d.append(a - b)
    d = np.concatenate(d)
    pair[other] = dict(mean_ndcg_diff=round(float(d.mean()), 4), se=round(float(d.std(ddof=1) / np.sqrt(len(d))), 4), n=len(d))
json.dump(pair, open(os.path.join(OUT, "paper_style_paired_ndcg.json"), "w"), indent=2); print(pair)
