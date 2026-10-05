"""Reproduce Tables 1-3 of Osadchiy et al. (2019) on the example data set {abcd, ade, de, ab}, input IF = {a, b}."""
from paper_algorithms import AR, TIC, PAR
meals = [set("abcd"), set("ade"), set("de"), set("ab")]
IF = {"a", "b"}
paper = {"AR (Table 1)": {"d": 2.50, "c": 1.96, "e": 0.29},
         "TIC (Table 2)": {"d": 3.00, "c": 2.00, "e": 0.50},
         "PAR (Table 3)": {"d": 5.8, "c": 4.2, "e": 1.0}}
models = {"AR (Table 1)": AR().fit(meals), "TIC (Table 2)": TIC().fit(meals), "PAR (Table 3)": PAR().fit(meals)}
ok = True
for name, m in models.items():
    got = dict(m.recommend(IF))
    line = ", ".join(f"{f}: {got.get(f, 0):.2f} (paper {v})" for f, v in paper[name].items())
    match = all(abs(got.get(f, 0) - v) < 0.06 for f, v in paper[name].items())
    ok &= match
    print(f"{name:14s} {line}   -> {'OK' if match else 'MISMATCH'}")
print("PAR model OD:", dict(models['PAR (Table 3)'].OD))
print("TIC model (unique meals):", {''.join(sorted(k)): {f: round(v, 2) for f, v in d.items()} for k, d in models['TIC (Table 2)'].TM.items()})
print("ALL TABLES REPRODUCED" if ok else "SOME TABLES NOT REPRODUCED")
