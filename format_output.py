from __future__ import annotations

from typing import Any

import yaml

CANDLE_YAML_FIELDS = (
    "candle_date_time_kst",
    "opening_price",
    "high_price",
    "low_price",
    "trade_price",
    "candle_acc_trade_volume",
)


def format_candles_yaml(candles: list[dict[str, Any]], market: str, interval: str) -> str:
    simplified = [
        {field: candle[field] for field in CANDLE_YAML_FIELDS if field in candle}
        for candle in reversed(candles)
    ]
    payload = {
        "market": market,
        "interval": interval,
        "count": len(simplified),
        "candles": simplified,
    }
    return yaml.dump(payload, allow_unicode=True, default_flow_style=False, sort_keys=False)
