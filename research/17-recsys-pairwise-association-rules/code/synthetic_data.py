"""Synthetic 'meal recall' transactions with planted food associations.

Purpose: a controlled testbed (the real Intake24 data used by Osadchiy et al. is not public).
Items are grouped into meal 'themes' (e.g. breakfast: tea, milk, toast, butter ...). A recall is a
union of 2-4 meal events; each event picks a theme (Zipf-like popularity) and then each food of the
theme independently with item-specific probability; a little background noise is added.
"""
import numpy as np

THEMES = {
 "breakfast_tea":   ["tea","milk","sugar","toast","butter","jam"],
 "breakfast_cereal":["cornflakes","milk","banana","orange_juice","yogurt"],
 "breakfast_cooked":["egg","bacon","sausage","baked_beans","toast","brown_sauce","coffee"],
 "sandwich_lunch":  ["sandwich","crisps","apple","cola","chocolate_bar"],
 "salad_lunch":     ["salad","dressing","bread_roll","water","tomato"],
 "soup_lunch":      ["soup","bread_roll","butter","water","cheese"],
 "pasta_dinner":    ["pasta","pasta_sauce","parmesan","garlic_bread","salad","red_wine"],
 "roast_dinner":    ["roast_meat","potato","carrot","peas","gravy","yorkshire_pud"],
 "curry_dinner":    ["curry","rice","naan","poppadom","lager"],
 "fish_chips":      ["fish","chips","mushy_peas","tartar_sauce","bread_butter","tea"],
 "dessert":         ["ice_cream","cake","custard","biscuit","fruit_salad"],
 "snack_drink":     ["coffee","biscuit","tea","chocolate_bar","crisps","fruit_juice"],
}
THEME_PROB = np.array([1.2,1.0,.7,1.5,.6,.5,.9,.6,.5,.4,.8,1.0]); THEME_PROB /= THEME_PROB.sum()


def generate(n_recalls=20000, n_filler=120, seed=0):
    rng = np.random.default_rng(seed)
    foods = sorted({f for t in THEMES.values() for f in t})
    foods += [f"other_food_{i:03d}" for i in range(n_filler)]       # long-tail catalogue
    idx = {f: i for i, f in enumerate(foods)}
    filler_p = 1.0 / (np.arange(1, n_filler + 1) ** 0.9); filler_p /= filler_p.sum()
    names = list(THEMES)
    X = np.zeros((n_recalls, len(foods)), dtype=np.uint8)
    for r in range(n_recalls):
        for _ in range(rng.integers(2, 5)):
            t = THEMES[names[rng.choice(len(names), p=THEME_PROB)]]
            for f in t:
                if rng.random() < 0.72:
                    X[r, idx[f]] = 1
        for j in rng.choice(n_filler, size=rng.integers(0, 3), p=filler_p, replace=False):
            X[r, len(foods) - n_filler + j] = 1
    return X, foods
