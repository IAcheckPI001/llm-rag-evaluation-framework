

from __future__ import annotations

from typing import Any, Dict

from app.core.metric_schemas import SystemLocalMetrics
from app.core.schemas import EvaluationRecord
from app.metrics.cost_metrics import calculate_total_tokens, estimate_cost_usd

# Roles => Calculate system-level metrics like latency, token counts, and estimated cost

def compute_system_metrics(
    record: EvaluationRecord,
    cost_config: Dict[str, Any],
) -> SystemLocalMetrics:
    total_tokens = calculate_total_tokens(
        input_tokens=record.input_tokens,
        output_tokens=record.output_tokens,
    )

    estimated_cost = estimate_cost_usd(
        input_tokens=record.input_tokens,
        output_tokens=record.output_tokens,
        model_name=record.model,
        cost_config=cost_config,
    )

    return SystemLocalMetrics(
        latency_ms=record.latency_ms,
        input_tokens=record.input_tokens,
        output_tokens=record.output_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=estimated_cost,
    )