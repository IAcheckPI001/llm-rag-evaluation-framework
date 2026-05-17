
from app.metrics.cost_metrics import calculate_total_tokens, estimate_cost_usd


def test_calculate_total_tokens():
    assert calculate_total_tokens(input_tokens=10, output_tokens=15) == 25
    assert calculate_total_tokens(input_tokens=None, output_tokens=15) == 15
    assert calculate_total_tokens(input_tokens=10, output_tokens=None) == 10
    assert calculate_total_tokens(input_tokens=None, output_tokens=None) == None

def test_estimate_cost_usd():
    config_cost = {
        "default_model": "gpt-4o-mini",
        "models": {
            "gpt-4o-mini": {
                "input_price_per_1m_tokens": 0.15,
                "output_price_per_1m_tokens": 0.60
            }
        }
    }

    assert estimate_cost_usd(input_tokens=10, output_tokens=15, model_name="gpt-4o-mini", cost_config=config_cost) == 10 / 1000000 * 0.15 + 15 / 1000000 * 0.60
    assert estimate_cost_usd(input_tokens=None, output_tokens=15, model_name="gpt-4o-mini", cost_config=config_cost) == 15 / 1000000 * 0.60
    assert estimate_cost_usd(input_tokens=10, output_tokens=None, model_name="gpt-4o-mini", cost_config=config_cost) == 10 / 1000000 * 0.15
    assert estimate_cost_usd(input_tokens=None, output_tokens=None, model_name="gpt-4o-mini", cost_config=config_cost) == None