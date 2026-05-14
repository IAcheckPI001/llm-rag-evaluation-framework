

from __future__ import annotations

from typing import Any, Dict

from app.core.schemas import EvaluationRecord
from app.services.mode_detector import detect_evaluation_mode

## Roles => Chuẩn hóa raw dict thành EvaluationRecord
# - Nhận raw dict (đến từ file JSONL, production logs, API response)
# - Dùng mode_detector để xác định evaluation mode
# - Tạo EvaluationRecord với các trường bắt buộc và optional
# - Trả về EvaluationRecord hoặc lỗi nếu thiếu trường bắt buộc hoặc kiểu dữ liệu không đúng

def normalize_raw_record(raw_record: Dict[str, Any]) -> EvaluationRecord:
    ground_truth = raw_record.get("ground_truth")
    expected_context_ids = raw_record.get("expected_context_ids")

    evaluation_mode = detect_evaluation_mode(
        ground_truth=ground_truth,
        expected_context_ids=expected_context_ids,
    )

    return EvaluationRecord(
        question_id=raw_record.get("question_id"),
        question=raw_record.get("question"),
        generated_answer=raw_record.get("generated_answer"),
        retrieved_contexts=raw_record.get("retrieved_contexts", []),
        ground_truth=ground_truth,
        expected_context_ids=expected_context_ids,
        evaluation_mode=evaluation_mode,
        label_status=raw_record.get("label_status", "unlabeled"),
        latency_ms=raw_record.get("latency_ms"),
        input_tokens=raw_record.get("input_tokens"),
        output_tokens=raw_record.get("output_tokens"),
        model=raw_record.get("model"),
        domain=raw_record.get("domain"),
        difficulty=raw_record.get("difficulty"),
        question_type=raw_record.get("question_type"),
        metadata=raw_record.get("metadata", {}),
    )