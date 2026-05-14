from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# Schemas is data contracts for the RAG evaluation framework

class EvaluationMode(str, Enum):
    LABELED_FULL = "labeled_full"
    REFERENCE_ANSWER_ONLY = "reference_answer_only"
    REFERENCE_FREE = "reference_free"


class LabelStatus(str, Enum):
    HUMAN_LABELED = "human_labeled"
    SYNTHETIC_LABELED = "synthetic_labeled"
    WEAK_LABELED = "weak_labeled"
    UNLABELED = "unlabeled"


class RetrievedContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    rank: int = Field(..., ge=1)
    score: Optional[float] = Field(default=None, ge=0.0)
    source: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("context_id", "text")
    @classmethod
    def strip_non_empty_string(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("field must not be empty")
        return value


class BenchmarkQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)

    ground_truth: Optional[str] = None
    expected_context_ids: Optional[List[str]] = None

    domain: Optional[str] = None
    difficulty: Optional[str] = None
    question_type: Optional[str] = None
    label_status: LabelStatus = LabelStatus.UNLABELED

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("question_id", "question")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("field must not be empty")
        return value

    @field_validator("ground_truth")
    @classmethod
    def strip_optional_ground_truth(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("expected_context_ids")
    @classmethod
    def validate_expected_context_ids(
        cls,
        value: Optional[List[str]],
    ) -> Optional[List[str]]:
        if value is None:
            return None

        cleaned = [item.strip() for item in value if item and item.strip()]
        if not cleaned:
            return None

        return list(dict.fromkeys(cleaned))


class RAGOutputRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    generated_answer: str = Field(..., min_length=1)
    retrieved_contexts: List[RetrievedContext] = Field(default_factory=list)

    latency_ms: Optional[float] = Field(default=None, ge=0)
    input_tokens: Optional[int] = Field(default=None, ge=0)
    output_tokens: Optional[int] = Field(default=None, ge=0)
    model: Optional[str] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("question_id", "question", "generated_answer")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("field must not be empty")
        return value

    @model_validator(mode="after")
    def sort_contexts_by_rank(self) -> "RAGOutputRecord":
        self.retrieved_contexts = sorted(
            self.retrieved_contexts,
            key=lambda ctx: ctx.rank,
        )
        return self


class EvaluationRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    generated_answer: str = Field(..., min_length=1)
    retrieved_contexts: List[RetrievedContext] = Field(default_factory=list)

    ground_truth: Optional[str] = None
    expected_context_ids: Optional[List[str]] = None

    evaluation_mode: EvaluationMode
    label_status: LabelStatus = LabelStatus.UNLABELED

    latency_ms: Optional[float] = Field(default=None, ge=0)
    input_tokens: Optional[int] = Field(default=None, ge=0)
    output_tokens: Optional[int] = Field(default=None, ge=0)
    model: Optional[str] = None

    domain: Optional[str] = None
    difficulty: Optional[str] = None
    question_type: Optional[str] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("question_id", "question", "generated_answer")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("field must not be empty")
        return value

    @model_validator(mode="after")
    def validate_mode_consistency(self) -> "EvaluationRecord":
        has_ground_truth = bool(self.ground_truth)
        has_expected_contexts = bool(self.expected_context_ids)

        if self.evaluation_mode == EvaluationMode.LABELED_FULL:
            if not has_ground_truth or not has_expected_contexts:
                raise ValueError(
                    "LABELED_FULL requires both ground_truth and expected_context_ids"
                )

        if self.evaluation_mode == EvaluationMode.REFERENCE_ANSWER_ONLY:
            if not has_ground_truth or has_expected_contexts:
                raise ValueError(
                    "REFERENCE_ANSWER_ONLY requires ground_truth and no expected_context_ids"
                )

        if self.evaluation_mode == EvaluationMode.REFERENCE_FREE:
            if has_ground_truth or has_expected_contexts:
                raise ValueError(
                    "REFERENCE_FREE should not contain ground_truth or expected_context_ids"
                )

        return self


class ValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: Optional[str] = None
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)