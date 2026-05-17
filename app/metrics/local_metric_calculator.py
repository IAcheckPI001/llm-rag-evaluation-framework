

from __future__ import annotations

from typing import Any, Dict, List

from app.core.metric_schemas import (
    LocalMetricResult,
    RetrievalLocalMetrics,
)
from app.core.schemas import EvaluationRecord
from app.metrics.retrieval_metrics import (
    hit_rate_at_k,
    mrr_at_k,
    precision_at_k,
    recall_at_k,
)
from app.metrics.system_metrics import compute_system_metrics


def extract_retrieved_context_ids(record: EvaluationRecord) -> List[str]:
    return [context.context_id for context in record.retrieved_contexts]


def compute_retrieval_local_metrics(
    record: EvaluationRecord,
    k: int,
) -> RetrievalLocalMetrics:
    retrieved_ids = extract_retrieved_context_ids(record)
    expected_ids = record.expected_context_ids

    retrieved_count = len(retrieved_ids)
    expected_count = len(expected_ids) if expected_ids else None

    if not expected_ids:
        return RetrievalLocalMetrics(
            retrieved_context_count=retrieved_count,
            expected_context_count=expected_count,
            can_compute_id_based_metrics=False,
            skip_reason="expected_context_ids missing",
        )

    return RetrievalLocalMetrics(
        true_hit_rate_at_k=hit_rate_at_k(retrieved_ids, expected_ids, k),
        mrr_at_k=mrr_at_k(retrieved_ids, expected_ids, k),
        precision_at_k=precision_at_k(retrieved_ids, expected_ids, k),
        recall_at_k=recall_at_k(retrieved_ids, expected_ids, k),
        retrieved_context_count=retrieved_count,
        expected_context_count=expected_count,
        can_compute_id_based_metrics=True,
        skip_reason=None,
    )


def compute_local_metrics_for_record(
    record: EvaluationRecord,
    k: int,
    cost_config: Dict[str, Any],
) -> LocalMetricResult:
    retrieval_metrics = compute_retrieval_local_metrics(record, k=k)
    system_metrics = compute_system_metrics(record, cost_config=cost_config)

    return LocalMetricResult(
        question_id=record.question_id,
        evaluation_mode=record.evaluation_mode,
        retrieval_metrics=retrieval_metrics,
        system_metrics=system_metrics,
        domain=record.domain,
        difficulty=record.difficulty,
        question_type=record.question_type,
        model=record.model,
    )