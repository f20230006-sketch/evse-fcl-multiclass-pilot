from __future__ import annotations

import numpy as np


def chronological_stratified_split_indices(
    labels: np.ndarray,
    timestamps: np.ndarray,
    test_size: float = 0.2,
) -> tuple[np.ndarray, np.ndarray]:
    """Hold out the latest records within every class.

    This preserves rare benign support while ensuring each class's test records
    occur after its training records.
    """

    labels = np.asarray(labels).astype(str)
    timestamps = np.asarray(timestamps, dtype=float)
    if len(labels) != len(timestamps):
        raise ValueError("labels and timestamps must have the same length")
    train_blocks: list[np.ndarray] = []
    test_blocks: list[np.ndarray] = []
    for label in np.unique(labels):
        indices = np.where(labels == label)[0]
        indices = indices[np.argsort(timestamps[indices], kind="stable")]
        if len(indices) == 1:
            train_blocks.append(indices)
            continue
        test_count = min(len(indices) - 1, max(1, int(round(len(indices) * test_size))))
        train_blocks.append(indices[:-test_count])
        test_blocks.append(indices[-test_count:])
    return np.concatenate(train_blocks), np.concatenate(test_blocks)


def operating_state_split_indices(
    operating_states: np.ndarray,
    holdout_state: str,
) -> tuple[np.ndarray, np.ndarray]:
    states = np.asarray(operating_states).astype(str)
    test = np.where(states == holdout_state)[0]
    train = np.where((states != holdout_state) & np.isin(states, ["charging", "idle"]))[0]
    if not len(train) or not len(test):
        raise ValueError(f"Cannot create operating-state holdout for '{holdout_state}'")
    return train, test


def leave_one_attack_out_indices(
    labels: np.ndarray,
    timestamps: np.ndarray,
    withheld_label: str,
    benign_names: tuple[str, ...] = ("benign", "normal", "b", "0"),
    benign_test_size: float = 0.3,
) -> tuple[np.ndarray, np.ndarray]:
    """Train on known attacks and early benign flows; test an unseen attack.

    The held-out set includes later benign records so false-positive rate and
    specificity remain measurable without reusing training records.
    """

    labels = np.asarray(labels).astype(str)
    timestamps = np.asarray(timestamps, dtype=float)
    benign = np.isin(np.char.lower(np.char.strip(labels)), benign_names)
    withheld = labels == withheld_label
    benign_indices = np.where(benign)[0]
    benign_indices = benign_indices[np.argsort(timestamps[benign_indices], kind="stable")]
    if len(benign_indices) < 2:
        raise ValueError("At least two benign rows are required for leave-one-attack-out evaluation")
    benign_test_count = min(
        len(benign_indices) - 1,
        max(1, int(round(len(benign_indices) * benign_test_size))),
    )
    test_benign = benign_indices[-benign_test_count:]
    train_benign = benign_indices[:-benign_test_count]
    train_attacks = np.where(~benign & ~withheld)[0]
    test_attacks = np.where(withheld)[0]
    if not len(train_attacks) or not len(test_attacks):
        raise ValueError(f"Withheld label '{withheld_label}' is absent or leaves no known attacks")
    return np.concatenate([train_benign, train_attacks]), np.concatenate([test_benign, test_attacks])


def evse_transfer_split_indices(
    evse_values: np.ndarray,
    train_evse: str,
) -> tuple[np.ndarray, np.ndarray]:
    evse = np.asarray(evse_values).astype(str)
    train = np.where(evse == train_evse)[0]
    test = np.where((evse != train_evse) & (evse != "unknown"))[0]
    if not len(train) or not len(test):
        raise ValueError(f"Cannot create EVSE transfer split for train EVSE '{train_evse}'")
    return train, test



def reproducible_non_iid_client_partitions(labels: np.ndarray, *, seed: int = 42) -> dict[str, np.ndarray]:
    """Assign each supplied row exactly once to five deterministic client profiles."""
    labels = np.asarray(labels).astype(str)
    names = ("reconnaissance_heavy", "flooding_heavy", "low_rate_rare_heavy", "mixed_open_set", "benign_starved")
    reconnaissance = {"Aggressive_Scan", "SYN_Stealth_Scan", "TCP_Port_Scan", "Service_Version_Detection", "OS_Fingerprinting"}
    flooding = {"SYN_Flood", "TCP_Flood", "UDP_Flood", "ICMP_Flood", "PSHACK_Flood", "SynonymousIP_Flood"}
    rare = {"Slowloris_Scan", "ICMP_Fragmentation", "Vulnerability_Scan"}
    rng = np.random.default_rng(seed)
    blocks = {name: [] for name in names}
    for label in sorted(set(labels)):
        rows = np.where(labels == label)[0].copy()
        rng.shuffle(rows)
        if label.strip().lower() in {"benign", "normal", "b", "0"}:
            fractions = np.array([0.55, 0.15, 0.10, 0.20, 0.0])
        elif label in reconnaissance:
            fractions = np.array([0.55, 0.10, 0.05, 0.20, 0.10])
        elif label in flooding:
            fractions = np.array([0.10, 0.55, 0.05, 0.20, 0.10])
        elif label in rare:
            fractions = np.array([0.05, 0.05, 0.55, 0.25, 0.10])
        else:
            fractions = np.array([0.10, 0.10, 0.10, 0.55, 0.15])
        counts = np.floor(fractions * len(rows)).astype(int)
        for position in np.argsort(-(fractions * len(rows) - counts))[: len(rows) - counts.sum()]:
            counts[position] += 1
        offset = 0
        for name, count in zip(names, counts):
            blocks[name].append(rows[offset:offset + count])
            offset += count
    result = {name: np.concatenate(parts) if parts else np.array([], dtype=int) for name, parts in blocks.items()}
    assigned = np.concatenate(list(result.values()))
    if len(assigned) != len(labels) or len(np.unique(assigned)) != len(labels):
        raise AssertionError("Non-IID partition must assign each source row exactly once")
    return result
