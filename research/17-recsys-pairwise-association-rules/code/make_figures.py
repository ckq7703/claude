import csv, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(__file__), "..", "results")
rows = list(csv.DictReader(open(os.path.join(OUT, "paper_style_results.csv"))))
col = {"Popularity": "#9aa9b8", "AR": "#4a93c9", "TIC": "#2777b6", "PAR": "#16598c"}
fig, axs = plt.subplots(1, 3, figsize=(13, 3.8))
for ax, (key, title) in zip(axs, (("ndcg15", "nDCG@15"), ("recall", "Recall (top 15)"), ("precision", "Precision (top 15)"))):
    for m, c in col.items():
        r = [x for x in rows if x["model"] == m]
        ax.plot([int(x["input_size"]) for x in r], [float(x[key]) for x in r], marker="o", color=c, label=m, lw=2.4 if m == "PAR" else 1.6)
    ax.set_title(title); ax.set_xlabel("Số món đầu vào"); ax.set_xticks(range(1, 6))
    for s in ("top", "right"): ax.spines[s].set_visible(False)
axs[0].legend(frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_paper_style_comparison.png"), dpi=150)
