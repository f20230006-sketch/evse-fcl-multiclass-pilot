"""Leakage-safe helpers for the supervisor rerun of the continual-FL EVSE study.

This module is deliberately dependency-light (NumPy/Pandas only) and is designed
as an overlay on the existing project. It does not modify the historical outputs.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

import numpy as np
import pandas as pd

from .data import (
    ABSOLUTE_TIMESTAMP_COLUMNS,
    PROVENANCE_COLUMNS,
    PreprocessState,
    fit_preprocess,
    transform_features,
)
from .metrics import binary_classification_metrics


DEFAULT_CAPTURE_IDENTIFIER_COLUMNS = (
    "id",
    "src_ip",
    "dst_ip",
    "src_mac",
    "dst_mac",
    "src_oui",
    "dst_oui",
    "expiration_id",
    "requested_server_name",
    "client_fingerprint",
    "server_fingerprint",
    "user_agent",
)

ROLE_FIT = "fitting"
ROLE_CAL = "calibration"
ROLE_EVAL = "evaluation"
ROLES = (ROLE_FIT, ROLE_CAL, ROLE_EVAL)


def _counts_for_partition(
    n: int,
    *,
    fitting_fraction: float,
    calibration_fraction: float,
    evaluation_fraction: float,
) -> tuple[int, int, int]:
    """Return fitting/calibration/evaluation counts with minimum-count safeguards.

    For n >= 3, all three roles get at least one row. For n == 2, one row is
    fitting and one is evaluation. For n == 1, the row remains fitting.
    """
    if n <= 0:
        return 0, 0, 0
    if n == 1:
        return 1, 0, 0
    if n == 2:
        return 1, 0, 1

    if not np.isclose(fitting_fraction + calibration_fraction + evaluation_fraction, 1.0):
        raise ValueError("Role fractions must sum to 1.0")

    n_eval = max(1, int(round(evaluation_fraction * n)))
    n_cal = max(1, int(round(calibration_fraction * n))) if calibration_fraction > 0 else 0
    n_fit = n - n_eval - n_cal

    while n_fit < 1 and n_eval > 1:
        n_eval -= 1
        n_fit += 1
    while n_fit < 1 and n_cal > 1:
        n_cal -= 1
        n_fit += 1
    if n_fit < 1:
        # Defensive fallback for unusual fractions.
        n_fit = 1
        remaining = n - 1
        n_cal = min(n_cal, remaining)
        n_eval = remaining - n_cal
    return n_fit, n_cal, n_eval


def client_for_each_row(client_assignments: dict[str, np.ndarray], n_rows: int) -> np.ndarray:
    clients = np.full(n_rows, "", dtype=object)
    seen = np.zeros(n_rows, dtype=int)
    for client, rows in client_assignments.items():
        rows = np.asarray(rows, dtype=int)
        clients[rows] = client
        seen[rows] += 1
    if not np.all(seen == 1):
        bad = np.where(seen != 1)[0]
        raise AssertionError(
            f"Each sampled row must belong to exactly one client; {len(bad)} violations found"
        )
    return clients.astype(str)


def assign_persistent_roles(
    labels: np.ndarray,
    client_assignments: dict[str, np.ndarray],
    *,
    seed: int,
    fitting_fraction: float = 0.65,
    calibration_fraction: float = 0.15,
    evaluation_fraction: float = 0.20,
) -> tuple[np.ndarray, dict]:
    """Assign one persistent role to each sampled row before task construction.

    Splitting is stratified independently within each (client, attack-label) block
    to preserve small attack families while preventing cross-role reuse.
    """
    labels = np.asarray(labels).astype(str)
    clients = client_for_each_row(client_assignments, len(labels))
    role = np.full(len(labels), "", dtype=object)
    rng = np.random.default_rng(seed + 20_000)
    blocks: list[dict] = []

    for client in sorted(client_assignments):
        client_rows = np.where(clients == client)[0]
        for label in sorted(set(labels[client_rows])):
            rows = client_rows[labels[client_rows] == label].copy()
            rng.shuffle(rows)
            n_fit, n_cal, n_eval = _counts_for_partition(
                len(rows),
                fitting_fraction=fitting_fraction,
                calibration_fraction=calibration_fraction,
                evaluation_fraction=evaluation_fraction,
            )
            fit_rows = rows[:n_fit]
            cal_rows = rows[n_fit : n_fit + n_cal]
            eval_rows = rows[n_fit + n_cal : n_fit + n_cal + n_eval]
            role[fit_rows] = ROLE_FIT
            role[cal_rows] = ROLE_CAL
            role[eval_rows] = ROLE_EVAL
            blocks.append(
                {
                    "client": client,
                    "label": label,
                    "rows": int(len(rows)),
                    "fitting": int(len(fit_rows)),
                    "calibration": int(len(cal_rows)),
                    "evaluation": int(len(eval_rows)),
                }
            )

    missing = np.where(role == "")[0]
    if len(missing):
        raise AssertionError(f"Persistent role was not assigned to {len(missing)} rows")

    counts = {name: int(np.sum(role == name)) for name in ROLES}
    return role.astype(str), {"overall": counts, "by_client_label": blocks}


def is_benign_array(labels: np.ndarray, benign_names: Iterable[str]) -> np.ndarray:
    benign = {str(v).strip().lower() for v in benign_names}
    normalized = np.char.lower(np.char.strip(np.asarray(labels).astype(str)))
    return np.isin(normalized, sorted(benign))


def build_persistent_tasks(
    labels: np.ndarray,
    client_assignments: dict[str, np.ndarray],
    roles: np.ndarray,
    tasks: list[tuple[str, set[str]]],
    *,
    benign_names: Iterable[str],
) -> list[dict]:
    labels = np.asarray(labels).astype(str)
    roles = np.asarray(roles).astype(str)
    benign = is_benign_array(labels, benign_names)
    prepared = []

    for task_name, family in tasks:
        current = benign | np.isin(labels, sorted(family))
        task = {"name": task_name, "labels": sorted(set(labels[current]) & set(family))}
        for role_name, key in ((ROLE_FIT, "train"), (ROLE_CAL, "calibration"), (ROLE_EVAL, "test")):
            task[key] = {}
            for client, client_rows in client_assignments.items():
                mask = current[client_rows] & (roles[client_rows] == role_name)
                task[key][client] = np.asarray(client_rows[mask], dtype=int)
        prepared.append(task)
    return prepared


def make_model_frame(frame: pd.DataFrame, label_column: str) -> tuple[pd.DataFrame, list[str]]:
    excluded = [
        *PROVENANCE_COLUMNS,
        *ABSOLUTE_TIMESTAMP_COLUMNS,
        *DEFAULT_CAPTURE_IDENTIFIER_COLUMNS,
    ]
    dropped = [column for column in excluded if column in frame.columns]
    return frame.drop(columns=dropped), dropped


def fit_frozen_preprocessor(
    frame: pd.DataFrame,
    label_column: str,
    preprocessing_fit_rows: np.ndarray,
    *,
    z_clip: float = 5.0,
) -> tuple[np.ndarray, PreprocessState, dict]:
    """Fit preprocessing only on historically permitted fitting rows, then freeze it."""
    model_frame, dropped = make_model_frame(frame, label_column)
    fit_rows = np.asarray(preprocessing_fit_rows, dtype=int)
    if not len(fit_rows):
        raise ValueError("Preprocessing requires at least one historically permitted fitting row")
    state = fit_preprocess(model_frame.iloc[fit_rows], label_column)
    x = transform_features(model_frame, label_column, state)
    if not np.isfinite(z_clip) or z_clip <= 0:
        raise ValueError("z_clip must be finite and positive")
    numeric_width = len(state.numeric_columns)
    x[:, :numeric_width] = np.clip(x[:, :numeric_width], -z_clip, z_clip)
    if not np.isfinite(x).all():
        raise FloatingPointError("Non-finite transformed features")
    metadata = {
        "numeric_z_clip": float(z_clip),
        "fit_rows": int(len(fit_rows)),
        "feature_count": int(x.shape[1]),
        "parameter_count_including_bias": int(x.shape[1] + 1),
        "dropped_columns": dropped,
        "numeric_columns": list(state.numeric_columns),
        "categorical_columns": list(state.categorical_columns),
        "feature_names": list(state.feature_names),
        "means": {k: float(v) for k, v in state.means.items()},
        "stds": {k: float(v) for k, v in state.stds.items()},
        "categories": {k: list(v) for k, v in state.categories.items()},
    }
    return x, state, metadata


def preprocess_state_to_dict(state: PreprocessState) -> dict:
    return asdict(state)


def split_audit(
    frame: pd.DataFrame,
    label_column: str,
    client_assignments: dict[str, np.ndarray],
    roles: np.ndarray,
    prepared_tasks: list[dict],
    preprocessing_fit_rows: np.ndarray,
    *,
    benign_names: Iterable[str],
) -> dict:
    labels = frame[label_column].astype(str).to_numpy()
    roles = np.asarray(roles).astype(str)
    n = len(frame)
    clients = client_for_each_row(client_assignments, n)

    if "__source_file__" not in frame.columns or "__source_row__" not in frame.columns:
        raise AssertionError("Provenance columns are required for leakage auditing")
    source_keys = frame["__source_file__"].astype(str) + "::" + frame["__source_row__"].astype(str)
    unique_source_keys = int(source_keys.nunique())
    if unique_source_keys != n:
        raise AssertionError(
            f"Source keys are not unique: {unique_source_keys} unique keys for {n} sampled rows"
        )

    role_sets = {r: set(np.where(roles == r)[0].tolist()) for r in ROLES}
    assert role_sets[ROLE_FIT].isdisjoint(role_sets[ROLE_CAL])
    assert role_sets[ROLE_FIT].isdisjoint(role_sets[ROLE_EVAL])
    assert role_sets[ROLE_CAL].isdisjoint(role_sets[ROLE_EVAL])
    assert len(set.union(*role_sets.values())) == n

    preprocessing_fit = set(np.asarray(preprocessing_fit_rows, dtype=int).tolist())
    if not preprocessing_fit.issubset(role_sets[ROLE_FIT]):
        raise AssertionError("Preprocessing fit rows must be a subset of persistent fitting rows")
    if preprocessing_fit & role_sets[ROLE_CAL]:
        raise AssertionError("Calibration rows leaked into preprocessing fit")
    if preprocessing_fit & role_sets[ROLE_EVAL]:
        raise AssertionError("Evaluation rows leaked into preprocessing fit")

    task_checks = []
    for task in prepared_tasks:
        train_rows = set()
        cal_rows = set()
        test_rows = set()
        for client in client_assignments:
            tr = set(np.asarray(task["train"][client], int).tolist())
            ca = set(np.asarray(task["calibration"][client], int).tolist())
            te = set(np.asarray(task["test"][client], int).tolist())
            if not tr.issubset(role_sets[ROLE_FIT]):
                raise AssertionError(f"{task['name']}: non-fitting row entered training")
            if not ca.issubset(role_sets[ROLE_CAL]):
                raise AssertionError(f"{task['name']}: non-calibration row entered calibration")
            if not te.issubset(role_sets[ROLE_EVAL]):
                raise AssertionError(f"{task['name']}: non-evaluation row entered evaluation")
            if tr & ca or tr & te or ca & te:
                raise AssertionError(f"{task['name']}/{client}: task-role overlap detected")
            train_rows |= tr
            cal_rows |= ca
            test_rows |= te
        task_checks.append(
            {
                "task": task["name"],
                "training_rows": len(train_rows),
                "calibration_rows": len(cal_rows),
                "evaluation_rows": len(test_rows),
                "train_cal_overlap": len(train_rows & cal_rows),
                "train_eval_overlap": len(train_rows & test_rows),
                "cal_eval_overlap": len(cal_rows & test_rows),
            }
        )

    benign = is_benign_array(labels, benign_names)
    unique_benign = {
        role_name: int(np.sum(benign & (roles == role_name))) for role_name in ROLES
    }
    unique_benign_eval_keys = int(source_keys[benign & (roles == ROLE_EVAL)].nunique())

    per_client_role = []
    for client in sorted(client_assignments):
        mask_client = clients == client
        for role_name in ROLES:
            mask = mask_client & (roles == role_name)
            per_client_role.append(
                {
                    "client": client,
                    "role": role_name,
                    "rows": int(mask.sum()),
                    "benign_rows": int((mask & benign).sum()),
                    "attack_rows": int((mask & ~benign).sum()),
                }
            )

    return {
        "status": "passed",
        "sampled_rows": n,
        "unique_source_keys": unique_source_keys,
        "persistent_role_counts": {r: len(role_sets[r]) for r in ROLES},
        "preprocessing_fit_rows": len(preprocessing_fit),
        "unique_benign_support_by_role": unique_benign,
        "unique_benign_evaluation_source_keys": unique_benign_eval_keys,
        "task_checks": task_checks,
        "per_client_role_counts": per_client_role,
        "assertions": {
            "each_source_row_unique": True,
            "each_row_exactly_one_client": True,
            "persistent_roles_disjoint": True,
            "preprocessing_fit_uses_fitting_only": True,
            "evaluation_excluded_from_preprocessing_fit": True,
            "calibration_excluded_from_preprocessing_fit": True,
            "task_train_cal_eval_disjoint": True,
        },
    }


def class_weights(labels: np.ndarray) -> np.ndarray:
    labels = np.asarray(labels, dtype=int)
    counts = np.bincount(labels, minlength=2)
    weights = np.ones(len(labels), dtype=float)
    for label, count in enumerate(counts):
        if count:
            weights[labels == label] = len(labels) / (2.0 * count)
    return weights


def sigmoid(scores: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(scores, -30.0, 30.0)))


def train_logistic_extended(
    features: np.ndarray,
    labels: np.ndarray,
    *,
    weights: np.ndarray,
    bias: float,
    epochs: int,
    learning_rate: float,
    l2: float = 1e-4,
    proximal_reference: tuple[np.ndarray, float] | None = None,
    proximal_mu: float = 0.0,
    ewc_terms: list[dict] | None = None,
    ewc_lambda: float = 0.0,
    max_gradient_norm: float = 1.0,
) -> tuple[np.ndarray, float]:
    """Class-weighted logistic update supporting full-parameter FedProx and EWC."""
    x = np.asarray(features, dtype=float)
    y = np.asarray(labels, dtype=float)
    coefficient = np.asarray(weights, dtype=float).copy()
    current_bias = float(bias)
    if len(y) == 0:
        return coefficient, current_bias

    sample_weight = class_weights(y.astype(int))
    normalizer = float(sample_weight.sum())
    ewc_terms = ewc_terms or []

    for _ in range(epochs):
        residual = (sigmoid(x @ coefficient + current_bias) - y) * sample_weight
        grad_w = (x.T @ residual) / normalizer + l2 * coefficient
        grad_b = float(residual.sum() / normalizer)

        if proximal_reference is not None and proximal_mu > 0:
            ref_w, ref_b = proximal_reference
            grad_w = grad_w + proximal_mu * (coefficient - np.asarray(ref_w, float))
            grad_b = grad_b + proximal_mu * (current_bias - float(ref_b))

        if ewc_terms and ewc_lambda > 0:
            for term in ewc_terms:
                grad_w = grad_w + ewc_lambda * term["fisher_w"] * (
                    coefficient - term["anchor_w"]
                )
                grad_b = grad_b + ewc_lambda * term["fisher_b"] * (
                    current_bias - term["anchor_b"]
                )

        gradient_norm = float(np.hypot(np.linalg.norm(grad_w), grad_b))
        if not np.isfinite(gradient_norm):
            raise FloatingPointError("Non-finite local gradient")
        if gradient_norm > max_gradient_norm:
            scale = max_gradient_norm / gradient_norm
            grad_w *= scale
            grad_b *= scale
        coefficient -= learning_rate * grad_w
        current_bias -= learning_rate * grad_b
        if not np.isfinite(coefficient).all() or not np.isfinite(current_bias):
            raise FloatingPointError("Non-finite local model parameters")

    return coefficient, current_bias


def predict_probability(features: np.ndarray, weights: np.ndarray, bias: float) -> np.ndarray:
    return sigmoid(np.asarray(features, dtype=float) @ np.asarray(weights, dtype=float) + float(bias))


def empirical_fisher_diagonal(
    features: np.ndarray,
    labels: np.ndarray,
    weights: np.ndarray,
    bias: float,
) -> tuple[np.ndarray, float]:
    """Empirical diagonal Fisher for binary logistic regression.

    This uses per-example score gradients of the conditional log likelihood.
    """
    x = np.asarray(features, dtype=float)
    y = np.asarray(labels, dtype=float)
    if len(y) == 0:
        return np.zeros_like(weights, dtype=float), 0.0
    p = predict_probability(x, weights, bias)
    score = y - p
    fisher_w = np.mean((score[:, None] * x) ** 2, axis=0)
    fisher_b = float(np.mean(score**2))
    scale = max(float(np.max(fisher_w)), fisher_b, 1e-12)
    fisher_w = fisher_w / scale
    fisher_b = fisher_b / scale
    return np.asarray(fisher_w, dtype=float), fisher_b


def calibration_balanced_accuracy(
    labels: np.ndarray,
    probabilities: np.ndarray,
) -> tuple[float, str]:
    labels = np.asarray(labels, dtype=int)
    if len(labels) == 0:
        return 0.5, "neutral_empty_calibration"
    if len(np.unique(labels)) < 2:
        return 0.5, "neutral_single_class_calibration"
    score = binary_classification_metrics(labels, np.asarray(probabilities) >= 0.5)[
        "balanced_accuracy"
    ]
    return float(score), "held_out_calibration"
