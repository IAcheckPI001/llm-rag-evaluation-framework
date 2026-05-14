
# LLM Evaluation Framework for RAG Systems

## 1. Overview

Build a RAG chatbot evaluation framework for real-world production, covering scenarios both with and without ground truth. The goal is to measure retrieval quality, response quality, hallucination, latency, and cost, while supporting error analysis for continuous system optimization.

## 2. Problem Statement

RAG chatbots in production typically log raw data like user questions, retrieved contexts, and token usage, but lack ground truth labels (reference answers or relevant context IDs).

This creates a gap in evaluation:
- **Retrieval Metrics** (Hit Rate@K, MRR) require labeled relevant IDs
- **Generation Metrics** (Correctness) require reference answers

This framework bridges this gap by supporting three evaluation modes:
- **Full Labeled**: Traditional evaluation with complete ground truth
- **Reference-only**: Evaluation when only gold answers are available
- **Reference-free**: Direct evaluation for production logs (LLM-as-a-judge)


## 3. Evaluation Pipeline

[Data Loading] -> [Pre-processing] -> [Evaluation] -> [Analysis] -> [Visualization]
      |                |                |               |              |
   Load/Val       Schema/Mode      Local/Judge     Failure Class    Report/Dash

## 4. Tech Stack

| Thành phần | Công nghệ / Tools | Lý do |
| --- | --- | --- |
| Core language | `python` | Phù hợp nhất cho RAG/evaluation/data pipeline |
| Data processing | `pandas` | Dễ xử lý JSONL/CSV, metric table, report |
| Schema validation | `pydantic` | Validate input/output rõ ràng |
| Local storage | `DuckDB` hoặc `SQLite` | Nhẹ, dễ demo, không cần server riêng |
| File format | `JSONL` + `Parquet` | JSONL dễ log, Parquet tốt cho analytics |
| Evaluation metrics | `Ragas` + `DeepEval` | Phù hợp faithfulness, relevancy, hallucination, RAG metrics |
| Local retrieval metrics | Custom Python functions | Hit Rate@K, MRR, Recall@K nên tự implement |
| API backend | `FastAPI` | Tạo evaluation service chuyên nghiệp |
| Dashboard | Streamlit | Nhanh, phù hợp portfolio/data dashboard |
| Config | YAML | Quản lý run config, threshold, model, metric |
| Report | Markdown + CSV + JSON | Dễ đọc, dễ lưu, dễ đưa GitHub |
| Container | `Docker` | Portfolio nhìn production-ready |
| Optional tracing | `Langfuse` hoặc `LangSmith` | Theo dõi trace, cost, latency, prompt/version |
| Optional CI/CD | GitHub Actions | Tự chạy eval nhỏ khi update pipeline |

## 5. Initial Project Structure

llm-rag-evaluation-framework/
│
├── app/
│   ├── core/                         # Configuration and Pydantic schemas
│   │   ├── config.py
│   │   └── schemas.py
│   │
│   ├── services/                     # Core logic (Data loading, Validation, Normalization)
│   │   ├── data_loader.py
│   │   ├── validator.py
│   │   ├── normalizer.py
│   │   └── mode_detector.py
│   │
│   ├── metrics/                      # Metric implementations (Retrieval, Cost, Local)
│   │   ├── local_metrics.py
│   │   ├── retrieval_metrics.py
│   │   └── cost_metrics.py
│   │
│   └── main.py                       # Entry point for the evaluation pipeline
│
├── configs/                          # YAML files for hyperparams and eval settings
│   └── eval_config.yaml
│
├── data/                             # Local data storage (Raw, Processed, and Results)
│   ├── raw/
│   │   └── sample_rag_logs.jsonl
│   │
│   ├── processed/
│   │   └── evaluation_records.parquet
│   │
│   └── results/
│       └── metric_results.parquet
│
├── reports/                          # Exported Markdown/PDF reports
│   └── sample_report.md
│
├── tests/                            # Pytest suite for core components
│   ├── test_validator.py
│   ├── test_normalizer.py
│   └── test_local_metrics.py
│
├── requirements.txt
├── README.md
└── Dockerfile

## 6. Installation

**Prerequisites**
[Docker Desktop](https://www.docker.com/products/docker-desktop/) installed

