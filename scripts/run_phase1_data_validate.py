

from __future__ import annotations

import json
import pandas as pd
from pathlib import Path

from app.services.data_loader import load_jsonl
from app.services.validator import validate_records
from app.services.exporter import export_records_to_parquet


def main() -> None:
    input_path = Path("data/raw/sample_rag_logs.jsonl")
    output_path = Path("data/processed/evaluation_records.parquet")
    validation_report_path = Path("data/results/validation_report.json")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    validation_report_path.parent.mkdir(parents=True, exist_ok=True)

    raw_records = load_jsonl(input_path)

    valid_records, validation_results = validate_records(raw_records)

    df = export_records_to_parquet(
        valid_records,
        output_path,
    )

    validation_report = {
        "total_records": len(raw_records),
        "valid_records": len(valid_records),
        "invalid_records": len(raw_records) - len(valid_records),
        "mode_distribution": (
            df["evaluation_mode"].value_counts().to_dict()
            if not df.empty
            else {}
        ),
        "validation_results": [
            result.model_dump(mode="json")
            for result in validation_results
        ],
    }

    with validation_report_path.open("w", encoding="utf-8") as file:
        json.dump(validation_report, file, ensure_ascii=False, indent=2)

    print("Phase 1 validation completed")
    print(f"Loaded records: {len(raw_records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Invalid records: {len(raw_records) - len(valid_records)}")
    print(f"Exported records: {output_path}")
    print(f"Validation report: {validation_report_path}")


if __name__ == "__main__":
    main()