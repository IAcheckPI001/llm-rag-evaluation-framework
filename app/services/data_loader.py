

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

## Roles:
# - Đọc JSONL file
# - Mỗi dòng parse thành dict
# - Bỏ qua dòng trống
# - Báo lỗi nếu dòng không phải JSON hợp lệ

def load_jsonl(file_path: str | Path) -> List[Dict[str, Any]]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    records: List[Dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {exc}"
                ) from exc

            records.append(record)

    return records