"""Exact re-implementation of the three recommenders compared in Osadchiy et al. (2019), Section 3.

  AR  - association rules (Algorithm 1): rules  antecedent-set => single consequent; score
        RF[f] += confidence * ms, with match score ms = |ant ∩ IF|^2 / (|ant| * |IF|)
  TIC - transactional item confidence (Algorithms 2-3), adapted from Roth et al. (2010)
  PAR - pairwise association rules (Algorithms 4-5):  RF[f] = sum(P[f]) * sum(W[f])
        P = CD[in,f] / OD[in] (conditional probability), W = OD[in] (frequency of the observed food)

Note on TIC: the paper's pseudocode (Alg. 2, line 9) writes c_f / c_m, but the worked example (Table 2) and the
text ("conditional probability of f given the rest of m") correspond to c_m / c_f, which is what is implemented here.
"""
from itertools import combinations
from collections import defaultdict
import numpy as np


# ---------------------------------------------------------------- PAR
class PAR:
    """Dictionary version (small data, matches the paper's pseudocode literally)."""
    def fit(self, meals):
        self.OD = defaultdict(int); self.CD = defaultdict(lambda: defaultdict(int))
        for m in meals:
            for f in m:
                self.OD[f] += 1
                for f1 in m:
                    if f1 != f: self.CD[f][f1] += 1
        return self

    def recommend(self, IF, k=None):
        P = defaultdict(list); W = defaultdict(list)
        for inf in IF:
            for f, c in self.CD.get(inf, {}).items():
                if f in IF: continue
                P[f].append(c / self.OD[inf]); W[f].append(self.OD[inf])
        RF = {f: sum(P[f]) * sum(W[f]) for f in P}
        out = sorted(RF.items(), key=lambda kv: -kv[1])
        return out[:k] if k else out


class PARMatrix:
    """Vectorised PAR for large experiments. X: binary (n_meals, n_foods)."""
    def fit(self, X):
        X = (X > 0).astype(np.float32)
        self.OD = X.sum(0)
        co = X.T @ X; np.fill_diagonal(co, 0); self.CD = co
        with np.errstate(divide="ignore", invalid="ignore"):
            self.Pm = np.where(self.OD[:, None] > 0, co / self.OD[:, None], 0.0)    # P[in, f]
        self.Wm = (co > 0) * self.OD[:, None]                                       # W[in, f]
        return self

    def scores(self, IF):
        IF = list(IF)
        s = self.Pm[IF].sum(0) * self.Wm[IF].sum(0)
        s[IF] = -1.0
        return s

    def recommend(self, IF, k=15):
        s = self.scores(IF)
        top = np.argpartition(-s, k)[:k]
        top = top[np.argsort(-s[top])]
        return [int(i) for i in top if s[i] > 0]


# ---------------------------------------------------------------- TIC
class TIC:
    def fit(self, meals):
        meals = [frozenset(m) for m in meals]
        uniq = set(meals)
        cnt_cache = {}

        def containing(s):
            if s not in cnt_cache: cnt_cache[s] = sum(1 for m in meals if s <= m)
            return cnt_cache[s]
        self.TM = {}
        for m in uniq:
            cm = containing(m)
            self.TM[m] = {f: cm / containing(m - {f}) for f in m}     # P(f | rest of m)
        return self

    def recommend(self, IF, k=None):
        IF = set(IF); RF = defaultdict(float)
        for m, d in self.TM.items():
            inter = len(m & IF)
            if inter:
                for f, c in d.items():
                    if f not in IF: RF[f] += inter * c
        out = sorted(RF.items(), key=lambda kv: -kv[1])
        return out[:k] if k else out


class TICSparse:
    """Vectorised TIC for larger data (X: binary meals x foods). Containment counts via bit masks."""
    def fit(self, X):
        X = (X > 0)
        n, m = X.shape
        masks = [int.from_bytes(np.packbits(X[:, j]).tobytes(), "big") for j in range(m)]
        def contain(items):
            v = (1 << (8 * ((n + 7) // 8))) - 1
            for j in items: v &= masks[j]
            return bin(v).count("1")
        U = np.unique(X, axis=0)
        TM = np.zeros(U.shape, dtype=np.float32)
        for i in range(U.shape[0]):
            items = np.flatnonzero(U[i])
            cm = contain(items)
            for f in items:
                rest = [j for j in items if j != f]
                TM[i, f] = cm / (contain(rest) if rest else n)
        self.U, self.TM = U.astype(np.float32), TM
        return self

    def scores(self, IF):
        IF = list(IF)
        inter = self.U[:, IF].sum(1)
        s = inter @ self.TM
        s[IF] = -1.0
        return s

    def recommend(self, IF, k=15):
        s = self.scores(IF)
        top = np.argpartition(-s, k)[:k]
        top = top[np.argsort(-s[top])]
        return [int(i) for i in top if s[i] > 0]


# ---------------------------------------------------------------- AR
class AR:
    """Association rules with multi-item antecedents and one consequent (Algorithm 1 of the paper).
    max_len bounds the size of mined itemsets; the paper uses unbounded FP-growth in Spark."""
    def fit(self, meals, min_count=1, max_len=None):
        meals = [frozenset(m) for m in meals]
        cnt = defaultdict(int)
        for m in meals:
            top = len(m) if max_len is None else min(len(m), max_len)
            for r in range(1, top + 1):
                for s in combinations(sorted(m), r): cnt[frozenset(s)] += 1
        self.rules = []                                        # (antecedent, consequent, confidence)
        for s, c in cnt.items():
            if c < min_count or len(s) < 2: continue
            for f in s:
                ant = s - {f}
                self.rules.append((ant, f, c / cnt[ant]))
        self.index = defaultdict(list)                         # inverted index: food -> rules whose antecedent has it
        for i, (ant, f, conf) in enumerate(self.rules):
            for a in ant: self.index[a].append(i)
        return self

    def recommend(self, IF, k=None):
        IF = set(IF); RF = defaultdict(float)
        seen = set()
        for a in IF:
            seen.update(self.index.get(a, ()))
        for i in seen:
            ant, f, conf = self.rules[i]
            if f in IF: continue
            inter = len(ant & IF)
            RF[f] += conf * inter ** 2 / (len(ant) * len(IF))
        out = sorted(RF.items(), key=lambda kv: -kv[1])
        return out[:k] if k else out
