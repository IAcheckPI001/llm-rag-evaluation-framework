
# This module provides functionality to export evaluation records to Parquet format.

from __future__ import annotations

import json
import pandas as pd
from pathlib import Path
from typing import List

from app.core.schemas import EvaluationRecord


NESTED_COLUMNS = {
    "retrieved_contexts",
    "expected_context_ids",
    "metadata",
}


def records_to_dataframe(records: List[EvaluationRecord]) -> pd.DataFrame:
    rows = []

    for record in records:
        row = record.model_dump(mode="json")

        for column in NESTED_COLUMNS:
            row[column] = json.dumps(
                row.get(column),
                ensure_ascii=False,
            )

        rows.append(row)

    return pd.DataFrame(rows)


def export_records_to_parquet(
    records: List[EvaluationRecord],
    output_path: str | Path,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df = records_to_dataframe(records)
    df.to_parquet(path, index=False)

    return df