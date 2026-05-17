
from app.services.data_loader import load_jsonl

def test_load_jsonl():
    records = load_jsonl("data/raw/sample_rag_logs.jsonl")
    assert len(records) > 0