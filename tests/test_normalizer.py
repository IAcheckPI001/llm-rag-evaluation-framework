

from app.services.normalizer import normalize_raw_record
from app.core.schemas import EvaluationMode


def test_normalize_labeled_full_record():
    raw = {
        "question_id": "q_001",
        "question": "Question?",
        "ground_truth": "Reference answer",
        "expected_context_ids": ["chunk_1"],
        "generated_answer": "Generated answer",
        "retrieved_contexts": [
            {
                "context_id": "chunk_1",
                "text": "Context",
                "rank": 1,
            }
        ],
    }

    record = normalize_raw_record(raw)

    assert record.question_id == "q_001"
    assert record.evaluation_mode == EvaluationMode.LABELED_FULL
    assert record.expected_context_ids == ["chunk_1"]


def test_normalize_reference_free_record():
    raw = {
        "question_id": "log_001",
        "question": "Question?",
        "generated_answer": "Generated answer",
        "retrieved_contexts": [
            {
                "context_id": "chunk_1",
                "text": "Context",
                "rank": 1,
            }
        ],
    }

    record = normalize_raw_record(raw)

    assert record.evaluation_mode == EvaluationMode.REFERENCE_FREE
    assert record.ground_truth is None
    assert record.expected_context_ids is None