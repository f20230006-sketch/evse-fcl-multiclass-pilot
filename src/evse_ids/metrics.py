from __future__ import annotations

import numpy as np


def binary_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float | int]:
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    accuracy = (tp + tn) / max(1, len(y_true))
    specificity = tn / (tn + fp) if (tn + fp) else 0.0
    balanced_accuracy = (recall + specificity) / 2
    denominator = float(np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)))
    matthews_correlation = ((tp * tn) - (fp * fn)) / denominator if denominator else 0.0

    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "specificity": float(specificity),
        "balanced_accuracy": float(balanced_accuracy),
        "matthews_correlation": float(matthews_correlation),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }


def label_distribution(labels: np.ndarray) -> dict[str, int]:
    values, counts = np.unique(labels.astype(str), return_counts=True)
    return {str(value): int(count) for value, count in zip(values, counts)}


def multiclass_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray, labels: list[str] | None = None) -> dict:
    """Return imbalance-aware multiclass metrics without requiring sklearn."""
    y_true = np.asarray(y_true).astype(str)
    y_pred = np.asarray(y_pred).astype(str)
    classes = labels or sorted(set(y_true.tolist()) | set(y_pred.tolist()))
    support = {label: int((y_true == label).sum()) for label in classes}
    per_class: dict[str, dict[str, float | int]] = {}
    precisions: list[float] = []
    recalls: list[float] = []
    f1s: list[float] = []
    weighted_f1 = 0.0
    for label in classes:
        tp = int(((y_true == label) & (y_pred == label)).sum())
        fp = int(((y_true != label) & (y_pred == label)).sum())
        fn = int(((y_true == label) & (y_pred != label)).sum())
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[label] = {"support": support[label], "precision": precision, "recall": recall, "f1": f1}
        precisions.append(precision); recalls.append(recall); f1s.append(f1)
        weighted_f1 += f1 * support[label]
    total = max(1, len(y_true))
    accuracy = float((y_true == y_pred).sum() / total)
    macro_precision = float(np.mean(precisions)) if precisions else 0.0
    macro_recall = float(np.mean(recalls)) if recalls else 0.0
    macro_f1 = float(np.mean(f1s)) if f1s else 0.0
    confusion = [[int(((y_true == actual) & (y_pred == predicted)).sum()) for predicted in classes] for actual in classes]
    return {
        "accuracy": accuracy,
        "precision_macro": macro_precision,
        "recall_macro": macro_recall,
        "macro_f1": macro_f1,
        "weighted_f1": float(weighted_f1 / total),
        "balanced_accuracy": macro_recall,
        "classes": classes,
        "per_class": per_class,
        "confusion_matrix": confusion,
    }
