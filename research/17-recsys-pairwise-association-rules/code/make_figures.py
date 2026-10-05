import csv, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from synthetic_data import generate
from par_recommender import PairwiseRuleRecommender
OUT = os.path.join(os.path.dirname(__file__), "..", "results")
rows = list(csv.DictReader(open(os.path.join(OUT, "results.csv"))))
C = {"blue": "#2777b6", "dark": "#16598c", "grey": "#9aa9b8", "orange": "#f05d32", "light": "#4a93c9"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})

# fig 1: model comparison (all contexts, N=10)
cmp_ = [r for r in rows if r["exp"] == "compare" and r["N"] == "10"]
fig, ax = plt.subplots(figsize=(8, 4.2))
names = [r["model"] for r in cmp_]; vals = [float(r["hit_rate"]) for r in cmp_]
cols = [C["grey"] if "Popularity" in n else C["light"] if "Item" in n else C["dark"] if "max conf" in n else C["blue"] for n in names]
b = ax.barh(names[::-1], vals[::-1], color=cols[::-1])
for rect, v in zip(b, vals[::-1]): ax.text(v + .008, rect.get_y() + rect.get_height() / 2, f"{v:.3f}", va="center")
ax.set_xlim(0, 1); ax.set_xlabel("Hit-rate@10 (hidden food found in top-10)"); ax.set_title("Synthetic meal recalls: model comparison")
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig1_model_comparison.png"), dpi=160); plt.close(fig)

# fig 2: context size
fig, ax = plt.subplots(figsize=(8, 4.2))
for m, c in (("Popularity", C["grey"]), ("ItemKNN (cosine)", C["light"]), ("PAR (max conf)", C["dark"]), ("PAR (sum conf)", C["orange"])):
    rr = [r for r in rows if r["exp"] == "context_size" and r["model"] == m]
    ax.plot([int(r["ctx"]) for r in rr], [float(r["hit_rate"]) for r in rr], marker="o", label=m, color=c)
ax.set_xlabel("Number of foods already selected (context size)"); ax.set_ylabel("Hit-rate@10"); ax.set_xticks([1, 2, 3, 5])
ax.set_title("Few-item contexts: collective model needs no user history"); ax.legend(frameon=False)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig2_context_size.png"), dpi=160); plt.close(fig)

# fig 3: training size
fig, ax = plt.subplots(figsize=(8, 4.2))
rr = [r for r in rows if r["exp"] == "train_size"]
ax.plot([int(r["ctx"]) for r in rr], [float(r["hit_rate"]) for r in rr], marker="o", color=C["dark"])
ax.set_xscale("log"); ax.set_xlabel("Training recalls (log scale)"); ax.set_ylabel("Hit-rate@10"); ax.set_title("Learning curve of the pairwise rule model")
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig3_training_size.png"), dpi=160); plt.close(fig)

# top rules
X, foods = generate(n_recalls=24000, seed=1)
m = PairwiseRuleRecommender().fit(X[:20000])
n = m.n_; rules = []
for a in range(len(foods)):
    for b_ in np.flatnonzero(m.conf_[a]):
        rules.append((a, b_, m.conf_[a, b_], m.conf_[a, b_] * m.cnt_[a] / n, m.lift_[a, b_]))
rules.sort(key=lambda t: -t[4])
with open(os.path.join(OUT, "top_rules_by_lift.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["antecedent", "consequent", "confidence", "support", "lift"])
    for a, b_, c, s, l in rules[:25]: w.writerow([foods[a], foods[b_], round(float(c), 4), round(float(s), 4), round(float(l), 3)])
print(len(rules), "rules;", [ (foods[a],foods[b_],round(float(l),2)) for a,b_,c,s,l in rules[:6]])
