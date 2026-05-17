
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.schemas import EvaluationMode


class RetrievalLocalMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    true_hit_rate_at_k: Optional[float] = None
    mrr_at_k: Optional[float] = None
    precision_at_k: Optional[float] = None
    recall_at_k: Optional[float] = None

    retrieved_context_count: int = 0
    expected_context_count: Optional[int] = None

    can_compute_id_based_metrics: bool = False
    skip_reason: Optional[str] = None


class SystemLocalMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    latency_ms: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    estimated_cost_usd: Optional[float] = None


class LocalMetricResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str
    evaluation_mode: EvaluationMode

    retrieval_metrics: RetrievalLocalMetrics
    system_metrics: SystemLocalMetrics

    domain: Optional[str] = None
    difficulty: Optional[str] = None
    question_type: Optional[str] = None
    model: Optional[str] = None

    metric_errors: List[str] = Field(default_factory=list)