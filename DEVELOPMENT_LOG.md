

# Project Development Log: LLM RAG Evaluation Framework

---

## Phase 1: Data Architecture & Strict Validation

### Target

To ensure that all data sources—including system logs, manually labeled ground truths, and simulation data—adhere to a consistent, and pre-defined structure

### Data pipeline

- **Input**: Read data logs from `sample_rag_logs.jsonl`
- **Process**: 
    - **Parsing**: Export nessesary fields (Query, Context, Response, Metadata)
    - **Mapping**: Mapping raw data to a standard Schema
    - **Validation**: Check the data type, mandatory fields, and define evaluation mode
- **Output**: Export file `evaluation_records.parquet`

### Tasklist

1. Create schemas.py by Pydantic
2. Create sample_rag_logs.jsonl
3. Write data_loader.py to read JSONL
4. Write validator.py to validate for each record
5. Write normalizer.py to normalize field
6. Write mode_detector.py to define evaluation mode
7. Export evaluation_records.parquet

### Output

| Ensure a consistent "Data Contract" across the entire Pipeline


## Phase 2: Local Metrics

### Target


### Data Pipeline

- **Input**: Read the normalized data from `evaluation_records.parquet`
- Process and calculate the metrics, including: `latency`, `token usage`, `cost estimate`, `Hit Rate@K`, `MRR`, `Recall@K`, `Precision@K`
- **Output**: Export the data component file `metric_results.parquet`

### Tasklist

1. Thêm metric schemas
2. Tạo cost_config.yaml
3. Viết loader đọc evaluation_records.parquet
4. Viết retrieval_metrics.py
5. Viết cost_metrics.py / system_metrics.py
6. Viết local_metric_calculator.py
7. Export local_metric_results.parquet + summary JSON
8. Viết unit tests cho từng metric

### Note: 

| Hit Rate@K, MRR, Precision@K, Recall@K are only calculated when the record has expected_context_ids

### Output

