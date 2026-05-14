
from __future__ import annotations
from typing import List, Optional

from app.core.schemas import EvaluationMode

## Roles:
# - Check ground_truth và expected_context_ids
# → quyết định evaluation_mode


def detect_evaluation_mode(
    ground_truth: Optional[str],
    expected_context_ids: Optional[List[str]],
) -> EvaluationMode:
    has_ground_truth = bool(ground_truth and ground_truth.strip())
    has_expected_contexts = bool(expected_context_ids)

    if has_ground_truth and has_expected_contexts:
        return EvaluationMode.LABELED_FULL

    if has_ground_truth and not has_expected_contexts:
        return EvaluationMode.REFERENCE_ANSWER_ONLY

    return EvaluationMode.REFERENCE_FREE