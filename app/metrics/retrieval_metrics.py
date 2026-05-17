

from __future__ import annotations

from typing import List, Optional


def hit_rate_at_k(
    retrieved_ids: List[str],
    expected_ids: Optional[List[str]],
    k: int,
) -> Optional[float]:
    if not expected_ids:
        return None

    top_k = retrieved_ids[:k]
    return 1.0 if any(context_id in expected_ids for context_id in top_k) else 0.0


def mrr_at_k(
    retrieved_ids: List[str],
    expected_ids: Optional[List[str]],
    k: int,
) -> Optional[float]:
    if not expected_ids:
        return None

    for index, context_id in enumerate(retrieved_ids[:k], start=1):
        if context_id in expected_ids:
            return 1.0 / index

    return 0.0


def precision_at_k(
    retrieved_ids: List[str],
    expected_ids: Optional[List[str]],
    k: int,
) -> Optional[float]:
    if not expected_ids:
        return None

    top_k = retrieved_ids[:k]

    if not top_k:
        return 0.0

    relevant_count = sum(1 for context_id in top_k if context_id in expected_ids)

    return relevant_count / len(top_k)


def recall_at_k(
    retrieved_ids: List[str],
    expected_ids: Optional[List[str]],
    k: int,
) -> Optional[float]:
    if not expected_ids:
        return None

    top_k = retrieved_ids[:k]
    retrieved_relevant = set(top_k).intersection(set(expected_ids))

    return len(retrieved_relevant) / len(set(expected_ids))