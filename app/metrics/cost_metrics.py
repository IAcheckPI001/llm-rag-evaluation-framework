
from __future__ import annotations

from typing import Any, Dict, Optional


def calculate_total_tokens(
    input_tokens: Optional[int],
    output_tokens: Optional[int],
) -> Optional[int]:
    if input_tokens is None and output_tokens is None:
        return None

    return (input_tokens or 0) + (output_tokens or 0)


def estimate_cost_usd(
    input_tokens: Optional[int],
    output_tokens: Optional[int],
    model_name: Optional[str],
    cost_config: Dict[str, Any],
) -> Optional[float]:
    if input_tokens is None and output_tokens is None:
        return None

    default_model = cost_config.get("default_model", "unknown")
    models = cost_config.get("models", {})

    selected_model = model_name or default_model
    model_config = models.get(selected_model) or models.get("unknown")

    if model_config is None:
        return None

    input_price = model_config.get("input_price_per_1m_tokens", 0.0)
    output_price = model_config.get("output_price_per_1m_tokens", 0.0)

    input_cost = (input_tokens or 0) / 1_000_000 * input_price
    output_cost = (output_tokens or 0) / 1_000_000 * output_price

    return input_cost + output_cost