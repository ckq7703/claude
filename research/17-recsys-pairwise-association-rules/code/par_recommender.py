"""Pairwise association rule (PAR) recommender - illustrative re-implementation.

This is NOT the authors' code. It implements the generic idea described in the abstract of
Osadchiy et al. (2019): a model of *collective* preferences built from transactions only,
using rules of the form  a -> b  between single items (pairs), with no user profile and no ratings.

Rule measures (Agrawal et al., 1993; Brin et al., 1997):
    support(a,b)    = P(a and b)
    confidence(a->b)= P(b | a)
    lift(a->b)      = P(b | a) / P(b)
"""
import numpy as np


class PairwiseRuleRecommender:
    def __init__(self, min_support=3e-4, min_confidence=3e-4, score="max"):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.score = score          # 'max' | 'sum' | 'noisy_or' | 'lift_max'

    def fit(self, X):
        """X: (n_transactions, n_items) binary numpy array."""
        X = (X > 0).astype(np.float32)
        n = X.shape[0]
        co = X.T @ X                              # co-occurrence counts
        cnt = np.diag(co).copy()                  # item counts
        np.fill_diagonal(co, 0)
        sup = co / n
        with np.errstate(divide="ignore", invalid="ignore"):
            conf = np.where(cnt[:, None] > 0, co / cnt[:, None], 0.0)   # conf[a, b] = P(b|a)
            lift = np.where(cnt[None, :] > 0, conf / (cnt[None, :] / n), 0.0)
        keep = (sup >= self.min_support) & (conf >= self.min_confidence)
        self.n_, self.cnt_ = n, cnt
        self.conf_ = np.where(keep, conf, 0.0)
        self.lift_ = np.where(keep, lift, 0.0)
        self.n_rules_ = int(keep.sum())
        self.pop_ = cnt / n
        return self

    def scores(self, context):
        """context: list of item indices already in the basket -> score vector over all items."""
        if len(context) == 0:
            return self.pop_.copy()
        C = self.conf_[context]                   # (|ctx|, n_items)
        if self.score == "max":
            s = C.max(axis=0)
        elif self.score == "sum":
            s = C.sum(axis=0)
        elif self.score == "noisy_or":
            s = 1.0 - np.prod(1.0 - C, axis=0)
        elif self.score == "lift_max":
            s = self.lift_[context].max(axis=0)
        else:
            raise ValueError(self.score)
        s = s.copy()
        s[context] = -1.0                         # never recommend what is already there
        return s

    def recommend(self, context, k=10):
        s = self.scores(context)
        s_tie = s + 1e-9 * self.pop_              # break ties by popularity
        s_tie[list(context)] = -np.inf
        return np.argsort(-s_tie)[:k]


class PopularityRecommender:
    def fit(self, X):
        self.pop_ = (X > 0).mean(axis=0)
        return self

    def recommend(self, context, k=10):
        s = self.pop_.copy()
        s[list(context)] = -np.inf
        return np.argsort(-s)[:k]


class ItemKNNRecommender:
    """Item-based CF with cosine similarity over the item-transaction matrix
    (Sarwar et al., 2001; Linden et al., 2003) - reference baseline."""
    def fit(self, X):
        X = (X > 0).astype(np.float32)
        co = X.T @ X
        norm = np.sqrt(np.diag(co)) + 1e-12
        self.sim_ = co / norm[:, None] / norm[None, :]
        np.fill_diagonal(self.sim_, 0)
        self.pop_ = X.mean(axis=0)
        return self

    def recommend(self, context, k=10):
        s = self.sim_[list(context)].sum(axis=0) if len(context) else self.pop_.copy()
        s = s + 1e-9 * self.pop_
        s[list(context)] = -np.inf
        return np.argsort(-s)[:k]
