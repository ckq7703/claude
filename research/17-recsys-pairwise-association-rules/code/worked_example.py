"""Hand-checkable example used in the report (section 4.4)."""
from itertools import combinations
T = [{"tea","milk","toast","butter"},{"tea","milk","biscuit"},{"coffee","toast","butter","jam"},
     {"tea","toast","butter"},{"coffee","milk","biscuit"},{"tea","milk","toast"}]
n = len(T); items = sorted(set().union(*T))
cnt = {i: sum(i in t for t in T) for i in items}
print("n =", n); print("item counts:", cnt)
pairs = {}
for a, b in combinations(items, 2):
    c = sum(a in t and b in t for t in T)
    if c: pairs[(a, b)] = c
print("pair counts:", pairs)
rules = []
for (a, b), c in pairs.items():
    for x, y in ((a, b), (b, a)):
        rules.append((x, y, c / n, c / cnt[x], (c / cnt[x]) / (cnt[y] / n)))
MINSUP = 2 / n; MINCONF = 0.5
kept = [r for r in rules if r[2] >= MINSUP and r[3] >= MINCONF]
print(f"rules kept with support>={MINSUP:.3f}, confidence>={MINCONF}:")
for x, y, s, c, l in sorted(kept, key=lambda r: (-r[3], r[0], r[1])):
    print(f"  {x:8s} -> {y:8s} supp={s:.3f} conf={c:.3f} lift={l:.3f}")
ctx = ["tea", "toast"]
score_max, score_sum = {}, {}
for x, y, s, c, l in kept:
    if x in ctx and y not in ctx:
        score_max[y] = max(score_max.get(y, 0), c); score_sum[y] = score_sum.get(y, 0) + c
print("context =", ctx)
print("max-confidence ranking:", sorted(score_max.items(), key=lambda kv: -kv[1]))
print("sum-confidence ranking:", sorted(score_sum.items(), key=lambda kv: -kv[1]))
