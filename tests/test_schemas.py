

import pytest
from pydantic import ValidationError

from app.core.schemas import RAGOutputRecord


def test_invalid_empty_generated_answer():
    with pytest.raises(ValidationError):
        RAGOutputRecord(
            question_id="q_001",
            question="Test question?",
            generated_answer="   ",
            retrieved_contexts=[
                {
                    "context_id": "chunk_1",
                    "text": "Some context",
                    "rank": 1,
                }
            ],
        )


def test_invalid_context_rank():
    with pytest.raises(ValidationError):
        RAGOutputRecord(
            question_id="q_001",
            question="Test question?",
            generated_answer="Answer",
            retrieved_contexts=[
                {
                    "context_id": "chunk_1",
                    "text": "Some context",
                    "rank": 0,
                }
            ],
        )


def test_contexts_are_sorted_by_rank():
    record = RAGOutputRecord(
        question_id="q_001",
        question="Test question?",
        generated_answer="Answer",
        retrieved_contexts=[
            {
                "context_id": "chunk_2",
                "text": "Context 2",
                "rank": 2,
            },
            {
                "context_id": "chunk_1",
                "text": "Context 1",
                "rank": 1,
            },
        ],
    )

    assert record.retrieved_contexts[0].context_id == "chunk_1"
    assert record.retrieved_contexts[1].context_id == "chunk_2"