"""Leave-one-item-out evaluation on synthetic meal recalls.

Task (mirrors the 'omitted food' use case of Intake24): hide ONE food of a held-out recall,
give the remaining foods as context, rank the catalogue, and check whether the hidden food is in the top-N.
Metrics: hit-rate@N (=recall of the single hidden item), precision@N = hit/N, MRR.
Also studies: context size (cold-start-like situation), support threshold, scoring function.
"""
import json, csv, os, time
import numpy as np
from synthetic_data import generate
from par_recommender import PairwiseRuleRecommender, PopularityRecommender, ItemKNNRecommender

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "..", "results")
os.makedirs(OUT, exist_ok=True)
X, foods = generate(n_recalls=24000, seed=1)
train, test = X[:20000], X[20000:]
rng = np.random.default_rng(7)


def make_cases(test, ctx_size=None, n_cases=4000):
    cases = []
    while len(cases) < n_cases:
        r = test[rng.integers(len(test))]
        items = np.flatnonzero(r)
        if len(items) < 2: continue
        hid = rng.choice(items)
        rest = [i for i in items if i != hid]
        if ctx_size is not None:
            if len(rest) < ctx_size: continue
            rest = list(rng.choice(rest, size=ctx_size, replace=False))
        cases.append((rest, hid))
    return cases


def evaluate(model, cases, N=10):
    hit = mrr = 0.0; t = time.perf_counter()
    for ctx, hid in cases:
        rec = model.recommend(ctx, N)
        pos = np.flatnonzero(rec == hid)
        if len(pos): hit += 1; mrr += 1.0 / (pos[0] + 1)
    n = len(cases)
    return dict(hit_rate=hit / n, precision=hit / n / N, mrr=mrr / n, ms_per_query=1000 * (time.perf_counter() - t) / n)


rows = []
# 1) model comparison, all contexts
cases = make_cases(test)
models = {
 "Popularity": PopularityRecommender().fit(train),
 "ItemKNN (cosine)": ItemKNNRecommender().fit(train),
 "PAR (max conf)": PairwiseRuleRecommender(score="max").fit(train),
 "PAR (sum conf)": PairwiseRuleRecommender(score="sum").fit(train),
 "PAR (noisy-or)": PairwiseRuleRecommender(score="noisy_or").fit(train),
 "PAR (max lift)": PairwiseRuleRecommender(score="lift_max").fit(train),
}
for name, m in models.items():
    for N in (5, 10):
        r = evaluate(m, cases, N); rows.append(dict(exp="compare", model=name, N=N, ctx="all", **r))

# 2) context size (cold-start-like: few foods selected so far)
for cs in (1, 2, 3, 5):
    cc = make_cases(test, ctx_size=cs)
    for name in ("Popularity", "ItemKNN (cosine)", "PAR (max conf)", "PAR (sum conf)"):
        r = evaluate(models[name], cc, 10); rows.append(dict(exp="context_size", model=name, N=10, ctx=cs, **r))

# 3) support / confidence threshold sweep
for th in (3e-4, 1e-3, 3e-3, 1e-2, 3e-2):
    m = PairwiseRuleRecommender(min_support=th, min_confidence=th, score="max").fit(train)
    r = evaluate(m, cases, 10); rows.append(dict(exp="threshold", model=f"PAR thr={th:g}", N=10, ctx="all", n_rules=m.n_rules_, **r))

# 4) training-set size (how much history is needed - collective model, not per-user)
for n in (200, 1000, 5000, 20000):
    m = PairwiseRuleRecommender(score="max").fit(train[:n])
    r = evaluate(m, cases, 10); rows.append(dict(exp="train_size", model="PAR (max conf)", N=10, ctx=n, n_rules=m.n_rules_, **r))

keys = sorted({k for r in rows for k in r}, key=lambda k: ["exp","model","N","ctx","n_rules","hit_rate","precision","mrr","ms_per_query"].index(k) if k in ["exp","model","N","ctx","n_rules","hit_rate","precision","mrr","ms_per_query"] else 99)
with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); [w.writerow(r) for r in rows]
json.dump(dict(n_train=len(train), n_test=len(test), n_items=len(foods), n_cases=len(cases),
               density=float(train.mean()), avg_items_per_recall=float(train.sum(1).mean())),
          open(os.path.join(OUT, "dataset_summary.json"), "w"), indent=2)
for r in rows:
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
