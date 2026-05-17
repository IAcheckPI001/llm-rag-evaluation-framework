

from __future__ import annotations

import json
import yaml
import pandas as pd
from pathlib import Path

from app.metrics.local_metric_calculator import compute_local_metrics_for_record
from app.services.parquet_loader import load_evaluation_records_from_parquet


def load_yaml(path: str | Path):
    with Path(path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main() -> None:
    input_path = Path("data/processed/evaluation_records.parquet")
    output_path = Path("data/results/local_metric_results.parquet")
    summary_path = Path("data/results/local_metric_summary.json")
    cost_config_path = Path("configs/cost_config.yaml")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cost_config = load_yaml(cost_config_path)
    records = load_evaluation_records_from_parquet(input_path)

    k = 5

    metric_results = [
        compute_local_metrics_for_record(
            record=record,
            k=k,
            cost_config=cost_config,
        )
        for record in records
    ]

    rows = [result.model_dump(mode="json") for result in metric_results]

    # Flatten nested metrics for easier Parquet analysis
    flat_rows = []

    for row in rows:
        flat_row = {
            "question_id": row["question_id"],
            "evaluation_mode": row["evaluation_mode"],
            "domain": row.get("domain"),
            "difficulty": row.get("difficulty"),
            "question_type": row.get("question_type"),
            "model": row.get("model"),
            **row["retrieval_metrics"],
            **row["system_metrics"],
            "metric_errors": json.dumps(row.get("metric_errors", []), ensure_ascii=False),
        }

        flat_rows.append(flat_row)

    df = pd.DataFrame(flat_rows)
    df.to_parquet(output_path, index=False)

    summary = {
        "total_records": len(df),
        "records_with_id_based_metrics": int(
            df["can_compute_id_based_metrics"].sum()
        ),
        "avg_latency_ms": (
            float(df["latency_ms"].mean())
            if "latency_ms" in df and not df["latency_ms"].dropna().empty
            else None
        ),
        "total_estimated_cost_usd": (
            float(df["estimated_cost_usd"].sum())
            if "estimated_cost_usd" in df
            else None
        ),
        "avg_true_hit_rate_at_k": (
            float(df["true_hit_rate_at_k"].dropna().mean())
            if not df["true_hit_rate_at_k"].dropna().empty
            else None
        ),
        "avg_mrr_at_k": (
            float(df["mrr_at_k"].dropna().mean())
            if not df["mrr_at_k"].dropna().empty
            else None
        ),
    }

    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, ensure_ascii=False, indent=2)

    print("Phase 2 local metrics completed")
    print(f"Loaded records: {len(records)}")
    print(f"Exported metric results: {output_path}")
    print(f"Exported summary: {summary_path}")


if __name__ == "__main__":
    main()