

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pandas as pd

from app.core.schemas import EvaluationRecord


JSON_COLUMNS = {
    "retrieved_contexts",
    "expected_context_ids",
    "metadata",
}


def load_evaluation_records_from_parquet(
    file_path: str | Path,
) -> List[EvaluationRecord]:
    df = pd.read_parquet(file_path)

    records: List[EvaluationRecord] = []

    for row in df.to_dict(orient="records"):
        for column in JSON_COLUMNS:
            value = row.get(column)

            if isinstance(value, str):
                row[column] = json.loads(value)

        records.append(EvaluationRecord(**row))

    return records