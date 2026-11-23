"""Two-stage rare reservation followed by the existing feasible class allocator."""
import numpy as np
from .continual_ablation import update_replay_buffer


def update_balanced_rare_buffer(existing, current, labels, *, capacity, rng,
                               rare_group, rare_fraction):
    if capacity < 0 or not 0 <= rare_fraction <= 1:
        raise ValueError('Invalid capacity or rare fraction')
    pool = np.unique(np.concatenate([np.asarray(existing, int), np.asarray(current, int)]))
    labels = np.asarray(labels).astype(str)
    rare = pool[np.isin(labels[pool], sorted(rare_group))]
    quota = int(np.floor(capacity * rare_fraction))
    reserved = update_replay_buffer([], rare, labels, capacity=min(quota, len(rare)),
                                    strategy='balanced', rng=rng)
    remaining = np.setdiff1d(pool, reserved)
    balanced = update_replay_buffer([], remaining, labels, capacity=capacity-len(reserved),
                                    strategy='balanced', rng=rng)
    result = np.sort(np.concatenate([reserved, balanced]).astype(int))
    assert len(result) == min(capacity, len(pool))
    return result, {'rare_quota_slots': quota, 'rare_candidates': len(rare),
                    'reserved_rows': reserved.tolist(), 'balanced_rows': balanced.tolist()}
