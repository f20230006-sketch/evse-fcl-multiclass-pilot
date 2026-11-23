import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[1]
METRICS = ["old_task_accuracy", "forgetting", "slowloris_recall", "worst_client_macro_recall"]

def select(df, space, methods):
    return df.loc[(df.environment == "federated") & (df.score_space == space)
                  & df.method.isin(methods)].copy()

def grid(df, methods):
    expected = {(m, f"order_{o}", s) for m in methods for o in range(1, 4) for s in range(42, 52)}
    rows = list(df[["method", "order", "seed"]].itertuples(index=False, name=None))
    if set(rows) != expected or len(rows) != len(expected):
        raise ValueError("Incomplete or duplicated method/order/seed grid")
    return df

def summary(df, metrics):
    return df.groupby(["method", "seed"])[metrics].mean().groupby("method").agg(["mean", "std"]) * 100

def paired(df, left, right, metric):
    a = df.pivot(index=["seed", "order"], columns="method", values=metric)
    d = (a[left] - a[right]).groupby("seed").mean() * 100
    if len(d) != 10 or not np.isfinite(d).all():
        raise ValueError("Expected ten complete seed pairs")
    mean = d.mean()
    half = t.ppf(.975, 9) * d.std(ddof=1) / np.sqrt(10)
    return mean, mean - half, mean + half

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT, help="Root containing historical report CSVs")
    p.add_argument("--out", type=Path, required=True, help="New directory for generated files")
    args = p.parse_args()
    root = args.root / "outputs"
    full = pd.read_csv(root / "cbrs_report_2026_10_28/all_per_run_metrics.csv")
    splits = pd.read_csv(root / "targeted_validation_report_2026_10_27/all_per_run_metrics.csv")
    extra = pd.read_csv(ROOT / "outputs/paper/evidence/exact_per_run.csv")
    exact_methods = ["class_balanced_60", "cbrs_60", "balanced_rare_60", "joint"]
    exact = grid(select(full, "original_type", exact_methods), exact_methods)
    extra = grid(select(extra, "original_type", exact_methods), exact_methods)
    keys = ["method", "seed", "order"]
    em = ["macro_precision", "macro_f1", "macro_average_precision"]
    i = summary(exact.merge(extra[keys + em], on=keys, validate="one_to_one"),
                [METRICS[0]] + em).loc[exact_methods]
    methods = ["no_replay", "uniform_60", "class_balanced_60", "cbrs_60", "protected_60",
               "balanced_rare_60", "ewc", "agem", "joint"]
    ii = summary(grid(select(full, "merged_scans", methods), methods), METRICS).loc[methods]
    records = []
    cols = ["mean_pp", "low95_pp", "high95_pp"]
    pair60 = ["balanced_rare_60", "class_balanced_60"]
    for split in range(42, 46):
        df = grid(select(splits[splits.split_seed == split], "merged_scans", pair60), pair60)
        for metric in METRICS[:1] + METRICS[2:3]:
            records.append((split, metric, *paired(df, *pair60, metric)))
    iii = pd.DataFrame(records, columns=["split", "metric"] + cols)
    records = []
    for capacity in (60, 300):
        pair = [f"balanced_rare_{capacity}", f"class_balanced_{capacity}"]
        df = grid(select(full, "merged_scans", pair), pair)
        for order in (1, 2, 3):
            for metric in METRICS[:1] + METRICS[2:3]:
                records.append((capacity, order, metric,
                                *paired(df[df.order == f"order_{order}"], *pair, metric)))
    figdata = pd.DataFrame(records, columns=["capacity", "order", "metric"] + cols)
    args.out.mkdir(parents=True, exist_ok=False)
    for name, df in [("table_I", i), ("table_II", ii)]:
        df.columns = [f"{metric}_{stat}_pct" for metric, stat in df.columns]
        df.to_csv(args.out / f"{name}.csv")
    iii.to_csv(args.out / "table_III.csv", index=False)
    figdata.to_csv(args.out / "figure_2.csv", index=False)
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.7))
    for ax, metric, title in zip(axes, [METRICS[0], METRICS[2]], ["Old-attack accuracy", "Slowloris recall"]):
        ax.axhline(0, color="gray", linewidth=.7)
        for capacity, off in [(60, -.08), (300, .08)]:
            g = figdata[(figdata.capacity == capacity) & (figdata.metric == metric)]
            mu = g.mean_pp.to_numpy()
            ax.errorbar(g.order + off, mu, yerr=[mu-g.low95_pp, g.high95_pp-mu],
                        fmt="o", capsize=3, label=f"B={capacity}")
        ax.set(title=title, xlabel="Attack order", xticks=[1, 2, 3])
    axes[0].set_ylabel("RBR minus class-balanced (percentage points)")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(args.out / "figure_2.pdf")
    plt.close(fig)

if __name__ == "__main__":
    main()
