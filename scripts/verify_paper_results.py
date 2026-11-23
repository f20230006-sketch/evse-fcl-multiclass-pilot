from pathlib import Path
import re, sys
import numpy as np
import pandas as pd

out, manuscript = map(Path, sys.argv[1:])
names = {"table_I": "exact_detection_results", "table_II": "allocation_results",
         "table_III": "federated_split_results"}
for table, tex in names.items():
    lines = (manuscript / "tables" / f"{tex}.tex").read_text().splitlines()
    expected = [tuple(map(float, re.findall(r"[+-]?[0-9]+\.[0-9]+", line)))
                for line in lines if " & " in line and re.search(r"[0-9]+\.[0-9]+", line)]
    a = pd.read_csv(out / f"{table}.csv").iloc[:, 2 if table == "table_III" else 1:]
    if table == "table_III":
        a = a.to_numpy().reshape(-1, 6)
    for row, target in zip(np.asarray(a), expected, strict=True):
        np.testing.assert_allclose(row[np.isfinite(row)], target, atol=.00501, rtol=0)
    print(f"{table}: matches printed values")
a = pd.read_csv(out / "figure_2.csv")
b = pd.read_csv(manuscript / "figures/order_effects_data.csv")
b["order"] = b.order.str.split("_").str[-1].astype(int)
a = a.merge(b, on=["capacity", "order", "metric"], validate="one_to_one")
assert len(a) == len(b) == 12
np.testing.assert_allclose(a[["mean_pp", "low95_pp", "high95_pp"]],
                           100*a[["mean_difference", "ci95_low", "ci95_high"]], atol=1e-7, rtol=0)
assert (out / "figure_2.pdf").read_bytes().startswith(b"%PDF")
print("Figure 2: all 12 point estimates and intervals match; PDF generated")
