"""Synthetic 'meal' transactions with planted food associations (testbed only).

The real Intake24 recalls used by Osadchiy et al. are not public, so the experiment runs on generated meals.
A meal is built from one theme (e.g. breakfast with tea: tea, milk, sugar, toast ...); each food of the theme is
included with probability p, then 0-2 random 'long tail' foods are added. Meals with fewer than 2 foods are discarded,
as in the paper's sampling rule."""
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


def generate(n_meals=20000, n_filler=120, p_item=0.78, seed=0):
    rng = np.random.default_rng(seed)
    foods = sorted({f for t in THEMES.values() for f in t}) + [f"other_food_{i:03d}" for i in range(n_filler)]
    idx = {f: i for i, f in enumerate(foods)}
    fp = 1.0 / (np.arange(1, n_filler + 1) ** 0.9); fp /= fp.sum()
    names = list(THEMES); rows = []
    while len(rows) < n_meals:
        x = np.zeros(len(foods), dtype=np.uint8)
        for f in THEMES[names[rng.choice(len(names), p=THEME_PROB)]]:
            if rng.random() < p_item: x[idx[f]] = 1
        for j in rng.choice(n_filler, size=rng.integers(0, 3), p=fp, replace=False):
            x[len(foods) - n_filler + j] = 1
        if x.sum() >= 2: rows.append(x)
    return np.array(rows), foods
