"""Helpers for controlled continual-FL replay and aggregation ablations."""

from __future__ import annotations

import numpy as np

from .metrics import binary_classification_metrics


def update_replay_buffer(
    existing,
    new_rows,
    labels,
    *,
    capacity,
    strategy,
    rng,
    protected_groups=None,
    minimum_fraction=0.2,
):
    """Return a bounded replay buffer with optional protected label groups."""
    if strategy not in {"none", "uniform", "balanced", "protected"}:
        raise ValueError(f"Unknown replay strategy: {strategy}")
    if strategy == "none" or capacity <= 0:
        return np.array([], dtype=int)
    pool = np.unique(np.concatenate([np.asarray(existing, int), np.asarray(new_rows, int)]))
    if len(pool) <= capacity:
        return pool
    if strategy == "uniform":
        return np.sort(rng.choice(pool, capacity, replace=False))
    pool_labels = np.asarray(labels)[pool].astype(str)
    if strategy == "protected":
        if not protected_groups:
            raise ValueError("protected_groups are required for protected replay")
        if not 0.0 <= minimum_fraction <= 1.0:
            raise ValueError("minimum_fraction must be between 0 and 1")
        quota = max(1, int(np.floor(capacity * minimum_fraction)))
        selected = []
        selected_set = set()
        for group in protected_groups:
            group = {str(label) for label in group}
            candidates = pool[np.isin(pool_labels, sorted(group))].copy()
            candidates = np.asarray(
                [row for row in candidates if int(row) not in selected_set], dtype=int
            )
            rng.shuffle(candidates)
            for row in candidates[: min(quota, len(candidates))]:
                selected.append(int(row))
                selected_set.add(int(row))
        remaining = np.asarray(
            [row for row in pool if int(row) not in selected_set], dtype=int
        )
        rng.shuffle(remaining)
        needed = capacity - len(selected)
        if needed > 0:
            selected.extend(int(row) for row in remaining[:needed])
        return np.sort(np.asarray(selected[:capacity], dtype=int))
    buckets = {}
    for label in sorted(set(pool_labels)):
        rows = pool[pool_labels == label].copy()
        rng.shuffle(rows)
        buckets[label] = rows.tolist()
    selected = []
    while len(selected) < capacity:
        progressed = False
        for label in sorted(buckets):
            if buckets[label] and len(selected) < capacity:
                selected.append(buckets[label].pop())
                progressed = True
        if not progressed:
            break
    return np.sort(np.asarray(selected, dtype=int))


def aggregation_weights(sample_counts, *, strategy="sample_size", reliability=None, drift=None):
    """Return FedAvg or n_i*BA_i/(1+d_i/median(d)) normalized weights."""
    counts = np.asarray(sample_counts, dtype=float)
    if np.any(counts < 0) or not counts.sum():
        raise ValueError("sample_counts must contain a positive total")
    if strategy == "sample_size":
        return counts / counts.sum()
    if strategy != "reliability_drift":
        raise ValueError(f"Unknown aggregation strategy: {strategy}")
    if reliability is None or drift is None:
        raise ValueError("reliability and drift are required")
    reliability = np.clip(np.asarray(reliability, float), 0.0, 1.0)
    drift = np.maximum(np.asarray(drift, float), 0.0)
    positive = drift[drift > 0]
    scale = float(np.median(positive)) if len(positive) else 1.0
    score = counts * np.maximum(reliability, 1e-6) / (1.0 + drift / scale)
    return score / score.sum()


def training_reliability(labels, probabilities):
    """In-sample balanced accuracy, used only as an aggregation ablation signal."""
    return float(binary_classification_metrics(labels, probabilities >= 0.5)["balanced_accuracy"])
