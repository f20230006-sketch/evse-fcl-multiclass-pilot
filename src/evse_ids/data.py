from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


DEFAULT_LABEL_CANDIDATES = (
    "label",
    "Label",
    "class",
    "Class",
    "attack",
    "Attack",
    "target",
    "Target",
)

ABSOLUTE_TIMESTAMP_COLUMNS = (
    "bidirectional_first_seen_ms",
    "bidirectional_last_seen_ms",
    "src2dst_first_seen_ms",
    "src2dst_last_seen_ms",
    "dst2src_first_seen_ms",
    "dst2src_last_seen_ms",
)

PROVENANCE_COLUMNS = (
    "__source_file__",
    "__source_row__",
    "__evse__",
    "__operating_state__",
)


def drop_absolute_timestamp_features(data: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Remove capture-time identifiers that can leak scenario chronology."""

    dropped = [column for column in ABSOLUTE_TIMESTAMP_COLUMNS if column in data.columns]
    return data.drop(columns=dropped), dropped


@dataclass
class DatasetBundle:
    features: np.ndarray
    labels: np.ndarray
    feature_names: list[str]
    label_column: str
    label_values: list[str]


@dataclass
class PreprocessState:
    numeric_columns: list[str]
    categorical_columns: list[str]
    feature_names: list[str]
    means: dict[str, float]
    stds: dict[str, float]
    categories: dict[str, list[str]]


def find_csv_files(path: str | Path) -> list[Path]:
    root = Path(path)
    if root.is_file() and root.suffix.lower() == ".csv":
        return [root]
    if root.is_dir():
        return sorted(root.rglob("*.csv"))
    raise FileNotFoundError(f"Dataset path not found: {root}")


def load_csv_dataset(path: str | Path, label_column: str | None = None) -> pd.DataFrame:
    files = find_csv_files(path)
    if not files:
        raise FileNotFoundError(f"No CSV files found under {path}")
    frames = [pd.read_csv(file) for file in files]
    data = pd.concat(frames, ignore_index=True)
    if label_column is None:
        label_column = infer_label_column(data)
    if label_column not in data.columns:
        raise ValueError(f"Label column '{label_column}' not found. Columns: {list(data.columns)}")
    return data


def load_sampled_csv_dataset(
    path: str | Path,
    label_column: str | None = None,
    max_rows_per_label: int = 2_000,
    seed: int = 42,
    chunksize: int = 100_000,
) -> pd.DataFrame:
    """Uniformly sample a bounded number of rows per label from large CSV files.

    Random priorities make the retained rows independent of source-file ordering.
    All benign rows are preserved because CICEVSE2024_NT is extremely imbalanced.
    """

    files = find_csv_files(path)
    if not files:
        raise FileNotFoundError(f"No CSV files found under {path}")
    rng = np.random.default_rng(seed)
    retained: dict[str, pd.DataFrame] = {}
    resolved_label = label_column

    for file in files:
        for chunk in pd.read_csv(file, chunksize=chunksize, low_memory=False):
            if resolved_label is None:
                resolved_label = infer_label_column(chunk)
            if resolved_label not in chunk.columns:
                if resolved_label == "Label":
                    chunk[resolved_label] = infer_label_from_filename(file.name)
                else:
                    raise ValueError(f"Label column '{resolved_label}' not found in {file}")
            chunk = chunk.copy()
            chunk["__sample_priority__"] = rng.random(len(chunk))
            for label, group in chunk.groupby(resolved_label, dropna=False):
                key = str(label)
                combined = pd.concat([retained.get(key, group.iloc[0:0]), group], ignore_index=True)
                if is_benign_label(key):
                    retained[key] = combined
                else:
                    retained[key] = combined.nsmallest(max_rows_per_label, "__sample_priority__")

    if not retained:
        raise ValueError("No dataset rows were retained.")
    sampled = pd.concat(retained.values(), ignore_index=True).drop_duplicates()
    sampled = sampled.sort_values("__sample_priority__").drop(columns=["__sample_priority__"])
    return sampled.reset_index(drop=True)


def load_sampled_csv_dataset_with_provenance(
    path: str | Path,
    label_column: str | None = None,
    max_rows_per_label: int = 2_000,
    seed: int = 42,
    chunksize: int = 100_000,
) -> pd.DataFrame:
    """Sample CSV records while retaining file/scenario metadata for safe splits.

    The provenance columns are split keys only and must be removed before model
    fitting. Source row numbers remain stable even when input files are chunked.
    """

    files = find_csv_files(path)
    if not files:
        raise FileNotFoundError(f"No CSV files found under {path}")
    root = Path(path)
    root = root if root.is_dir() else root.parent
    rng = np.random.default_rng(seed)
    retained: dict[str, pd.DataFrame] = {}
    resolved_label = label_column

    for file in files:
        row_offset = 0
        relative_file = file.relative_to(root).as_posix()
        lower_name = file.name.lower()
        evse = "EVSE-A" if "evse-a" in lower_name else "EVSE-B" if "evse-b" in lower_name else "unknown"
        operating_state = (
            "charging" if "charging" in lower_name
            else "idle" if "idle" in lower_name
            else "malicious_ev" if "maliciousev" in lower_name
            else "unknown"
        )
        for chunk in pd.read_csv(file, chunksize=chunksize, low_memory=False):
            if resolved_label is None:
                resolved_label = infer_label_column(chunk)
            if resolved_label not in chunk.columns:
                if resolved_label == "Label":
                    chunk[resolved_label] = infer_label_from_filename(file.name)
                else:
                    raise ValueError(f"Label column '{resolved_label}' not found in {file}")
            chunk = chunk.copy()
            chunk["__source_file__"] = relative_file
            chunk["__source_row__"] = np.arange(row_offset, row_offset + len(chunk), dtype=np.int64)
            chunk["__evse__"] = evse
            chunk["__operating_state__"] = operating_state
            row_offset += len(chunk)
            chunk["__sample_priority__"] = rng.random(len(chunk))
            for label, group in chunk.groupby(resolved_label, dropna=False):
                key = str(label)
                combined = pd.concat([retained.get(key, group.iloc[0:0]), group], ignore_index=True)
                if is_benign_label(key):
                    retained[key] = combined
                else:
                    retained[key] = combined.nsmallest(max_rows_per_label, "__sample_priority__")

    if not retained:
        raise ValueError("No dataset rows were retained.")
    sampled = pd.concat(retained.values(), ignore_index=True)
    sampled = sampled.sort_values("__sample_priority__").drop(columns=["__sample_priority__"])
    return sampled.reset_index(drop=True)


def infer_label_from_filename(filename: str) -> str:
    """Map official CICEVSE2024 scenario filenames to stable labels."""
    name = filename.lower().replace("_", "-")
    mappings = (
        ("benign", "Benign"),
        ("aggressive", "Aggressive_Scan"),
        ("icmp-fragmentation", "ICMP_Fragmentation"),
        ("icmp-flood", "ICMP_Flood"),
        ("os-fingerprint", "OS_Fingerprinting"),
        ("port-scan", "TCP_Port_Scan"),
        ("portscan", "TCP_Port_Scan"),
        ("push-ack", "PSHACK_Flood"),
        ("service-detection", "Service_Version_Detection"),
        ("slowloris", "Slowloris_Scan"),
        ("syn-stealth", "SYN_Stealth_Scan"),
        ("synonymous-ip", "SynonymousIP_Flood"),
        ("syn-flood", "SYN_Flood"),
        ("tcp-flood", "TCP_Flood"),
        ("udp-flood", "UDP_Flood"),
        ("vulnerability-scan", "Vulnerability_Scan"),
    )
    for token, label in mappings:
        if token in name:
            return label
    raise ValueError(f"Could not infer an official CICEVSE label from filename: {filename}")


def stratified_train_test_split_indices(
    labels: np.ndarray,
    test_size: float = 0.2,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Split every observed class into train/test partitions when possible."""

    rng = np.random.default_rng(seed)
    labels = np.asarray(labels).astype(str)
    train_blocks: list[np.ndarray] = []
    test_blocks: list[np.ndarray] = []
    for label in np.unique(labels):
        indices = np.where(labels == label)[0]
        rng.shuffle(indices)
        if len(indices) == 1:
            train_blocks.append(indices)
            continue
        test_count = min(len(indices) - 1, max(1, int(round(len(indices) * test_size))))
        test_blocks.append(indices[:test_count])
        train_blocks.append(indices[test_count:])
    train = np.concatenate(train_blocks) if train_blocks else np.array([], dtype=int)
    test = np.concatenate(test_blocks) if test_blocks else np.array([], dtype=int)
    rng.shuffle(train)
    rng.shuffle(test)
    return train, test


def infer_label_column(data: pd.DataFrame) -> str:
    for candidate in DEFAULT_LABEL_CANDIDATES:
        if candidate in data.columns:
            return candidate
    raise ValueError(
        "Could not infer label column. Pass --label-column explicitly. "
        f"Available columns: {list(data.columns)}"
    )


def fit_preprocess(data: pd.DataFrame, label_column: str) -> PreprocessState:
    feature_df = data.drop(columns=[label_column])
    numeric_columns = [
        column for column in feature_df.columns if pd.api.types.is_numeric_dtype(feature_df[column])
    ]
    categorical_columns = [column for column in feature_df.columns if column not in numeric_columns]

    means: dict[str, float] = {}
    stds: dict[str, float] = {}
    categories: dict[str, list[str]] = {}
    feature_names: list[str] = []

    for column in numeric_columns:
        values = pd.to_numeric(feature_df[column], errors="coerce")
        mean = float(values.mean()) if not np.isnan(values.mean()) else 0.0
        std = float(values.std()) if not np.isnan(values.std()) and values.std() > 0 else 1.0
        means[column] = mean
        stds[column] = std
        feature_names.append(column)

    for column in categorical_columns:
        cats = sorted(feature_df[column].fillna("__missing__").astype(str).unique().tolist())
        categories[column] = cats
        feature_names.extend([f"{column}={cat}" for cat in cats])

    return PreprocessState(
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        feature_names=feature_names,
        means=means,
        stds=stds,
        categories=categories,
    )


def transform_features(data: pd.DataFrame, label_column: str, state: PreprocessState) -> np.ndarray:
    feature_blocks: list[np.ndarray] = []

    for column in state.numeric_columns:
        values = pd.to_numeric(data[column], errors="coerce").fillna(state.means[column]).to_numpy(float)
        feature_blocks.append(((values - state.means[column]) / state.stds[column]).reshape(-1, 1))

    for column in state.categorical_columns:
        values = data[column].fillna("__missing__").astype(str)
        cats = state.categories[column]
        encoded = np.zeros((len(data), len(cats)), dtype=float)
        index = {cat: pos for pos, cat in enumerate(cats)}
        for row, value in enumerate(values):
            if value in index:
                encoded[row, index[value]] = 1.0
        feature_blocks.append(encoded)

    if not feature_blocks:
        raise ValueError("No usable feature columns found.")
    return np.hstack(feature_blocks)


def make_dataset_bundle(data: pd.DataFrame, label_column: str | None = None) -> tuple[DatasetBundle, PreprocessState]:
    label_column = label_column or infer_label_column(data)
    state = fit_preprocess(data, label_column)
    features = transform_features(data, label_column, state)
    labels = data[label_column].fillna("__missing__").astype(str).to_numpy()
    return (
        DatasetBundle(
            features=features,
            labels=labels,
            feature_names=state.feature_names,
            label_column=label_column,
            label_values=sorted(pd.Series(labels).unique().tolist()),
        ),
        state,
    )


def train_test_split_indices(n_rows: int, test_size: float = 0.2, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    indices = np.arange(n_rows)
    rng.shuffle(indices)
    test_count = max(1, int(round(n_rows * test_size)))
    test_idx = indices[:test_count]
    train_idx = indices[test_count:]
    return train_idx, test_idx


def is_benign_label(label: str, benign_labels: Iterable[str] | None = None) -> bool:
    benign = {value.lower() for value in (benign_labels or ("benign", "normal", "b", "0"))}
    return str(label).strip().lower() in benign


def labels_to_binary(labels: np.ndarray, benign_labels: Iterable[str] | None = None) -> np.ndarray:
    return np.array([0 if is_benign_label(label, benign_labels) else 1 for label in labels], dtype=int)


def synthetic_evse_dataset(n_rows: int = 1200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    labels = rng.choice(["benign", "dos", "replay", "fuzzing"], size=n_rows, p=[0.68, 0.14, 0.1, 0.08])
    base_current = rng.normal(30, 5, size=n_rows)
    base_voltage = rng.normal(400, 12, size=n_rows)
    base_power = base_current * base_voltage / 1000 + rng.normal(0, 0.8, size=n_rows)
    packet_rate = rng.normal(60, 10, size=n_rows)
    error_rate = rng.normal(0.01, 0.005, size=n_rows)

    attack_mask = labels != "benign"
    dos_mask = labels == "dos"
    replay_mask = labels == "replay"
    fuzz_mask = labels == "fuzzing"
    packet_rate[dos_mask] += rng.normal(90, 20, size=dos_mask.sum())
    error_rate[fuzz_mask] += rng.normal(0.2, 0.04, size=fuzz_mask.sum())
    base_power[replay_mask] += rng.normal(8, 2, size=replay_mask.sum())
    base_current[attack_mask] += rng.normal(3, 1.5, size=attack_mask.sum())

    return pd.DataFrame(
        {
            "current": base_current,
            "voltage": base_voltage,
            "power": base_power,
            "packet_rate": packet_rate,
            "error_rate": np.clip(error_rate, 0, None),
            "connector_state": rng.choice(["charging", "idle", "auth"], size=n_rows),
            "label": labels,
        }
    )
