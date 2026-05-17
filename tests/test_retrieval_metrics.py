

from app.metrics.retrieval_metrics import (
    hit_rate_at_k,
    mrr_at_k,
    precision_at_k,
    recall_at_k
)

def test_hit_rate_at_k():

    retrieved_ids = ["ctx1", "ctx2", "ctx3"]
    expected_ids = ["ctx2", "ctx4"]
    k = 3

    assert hit_rate_at_k(retrieved_ids, expected_ids, k) == 1.0

def test_mrr_at_k():

    retrieved_ids = ["ctx1", "ctx2", "ctx3"]
    expected_ids = ["ctx2", "ctx4"]
    k = 3
    assert mrr_at_k(retrieved_ids, expected_ids, k) == 1.0 / 2

def test_precision_at_k():

    retrieved_ids = ["ctx1", "ctx2", "ctx3"]
    expected_ids = ["ctx2", "ctx4"]
    k = 3
    assert precision_at_k(retrieved_ids, expected_ids, k) == 1/3

def test_recall_at_k():

    retrieved_ids = ["ctx1", "ctx2", "ctx3"]
    expected_ids = ["ctx2", "ctx4"]
    k = 3
    assert recall_at_k(retrieved_ids, expected_ids, k) == 0.5

def test_metrics_with_missing_expected_ids():

    retrieved_ids = ["ctx1", "ctx2", "ctx3"]
    expected_ids = None
    k = 3

    assert hit_rate_at_k(retrieved_ids, expected_ids, k) is None
    assert mrr_at_k(retrieved_ids, expected_ids, k) is None
    assert precision_at_k(retrieved_ids, expected_ids, k) is None
    assert recall_at_k(retrieved_ids, expected_ids, k) is None