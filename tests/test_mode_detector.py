
from app.core.schemas import EvaluationMode
from app.services.mode_detector import detect_evaluation_mode

def test_detect_labeled_full_mode():
    mode = detect_evaluation_mode("answer", ["chunk_1"])
    assert mode == EvaluationMode.LABELED_FULL


def test_detect_reference_answer_only_mode():
    mode = detect_evaluation_mode("answer", None)
    assert mode == EvaluationMode.REFERENCE_ANSWER_ONLY


def test_detect_reference_free_mode():
    mode = detect_evaluation_mode(None, None)
    assert mode == EvaluationMode.REFERENCE_FREE