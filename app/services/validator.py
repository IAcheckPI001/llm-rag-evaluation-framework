

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from pydantic import ValidationError

from app.core.schemas import EvaluationRecord, ValidationResult
from app.services.normalizer import normalize_raw_record


## Roles:
# - Nhận raw dict
# - Dùng Pydantic validate thành RAGOutputRecord-like input
# - Trả về valid records và validation results

## Handling cases:
# Raw dict
# → normalizer detect mode
# → tạo EvaluationRecord
# → nếu tạo được thì valid
# → nếu lỗi Pydantic thì invalid

def validate_records(
    raw_records: List[Dict[str, Any]],
) -> Tuple[List[EvaluationRecord], List[ValidationResult]]:
    valid_records: List[EvaluationRecord] = []
    validation_results: List[ValidationResult] = []

    for raw_record in raw_records:
        question_id = raw_record.get("question_id")

        try:
            evaluation_record = normalize_raw_record(raw_record)

            valid_records.append(evaluation_record)
            validation_results.append(
                ValidationResult(
                    question_id=evaluation_record.question_id,
                    is_valid=True,
                    errors=[],
                    warnings=[],
                )
            )

        except ValidationError as exc:
            validation_results.append(
                ValidationResult(
                    question_id=question_id,
                    is_valid=False,
                    errors=[str(error) for error in exc.errors()],
                    warnings=[],
                )
            )

        except Exception as exc:
            validation_results.append(
                ValidationResult(
                    question_id=question_id,
                    is_valid=False,
                    errors=[str(exc)],
                    warnings=[],
                )
            )

    return valid_records, validation_results