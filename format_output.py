from __future__ import annotations

import csv
import io
from typing import Any

CANDLE_CSV_FIELDS = (
    ("datetime", "candle_date_time_kst"),
    ("open", "opening_price"),
    ("high", "high_price"),
    ("low", "low_price"),
    ("close", "trade_price"),
    ("volume", "candle_acc_trade_volume"),
)


def format_candles_csv(candles: list[dict[str, Any]], market: str, interval: str) -> str:
    output = io.StringIO()
    output.write(f"# market={market},interval={interval},count={len(candles)}\n")

    writer = csv.writer(output, lineterminator="\n")
    writer.writerow([column for column, _ in CANDLE_CSV_FIELDS])

    for candle in reversed(candles):
        writer.writerow([candle.get(source, "") for _, source in CANDLE_CSV_FIELDS])

    return output.getvalue()
