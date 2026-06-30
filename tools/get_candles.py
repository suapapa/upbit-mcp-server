from typing import Any, Literal, Optional, cast

from fastmcp import Context

from format_output import format_candles_yaml
from mcp_context import ctx_error, ctx_info, ctx_warning
from upbit_client import format_api_error, get_public_client, to_serializable

CANDLE_METHODS = {
    "second": "list_seconds",
    "day": "list_days",
    "week": "list_weeks",
    "month": "list_months",
    "year": "list_years",
}

MinuteUnit = Literal[1, 3, 5, 10, 15, 30, 60, 240]

MINUTE_UNITS: dict[str, MinuteUnit] = {
    "minute1": 1,
    "minute3": 3,
    "minute5": 5,
    "minute10": 10,
    "minute15": 15,
    "minute30": 30,
    "minute60": 60,
    "minute240": 240,
}


async def get_candles(
    market: str,
    interval: Literal[
        "second",
        "minute1",
        "minute3",
        "minute5",
        "minute10",
        "minute15",
        "minute30",
        "minute60",
        "minute240",
        "day",
        "week",
        "month",
        "year",
    ],
    count: int = 200,
    to: Optional[str] = None,
    ctx: Context | None = None,
) -> str:
    """
    업비트에서 캔들스틱 데이터를 조회합니다.

    Args:
        market (str): 마켓 코드 (예: KRW-BTC)
        interval (str): 시간 간격 (second, minute1~minute240, day, week, month, year)
        count (int): 캔들 개수 (최대 200)
        to (str, optional): 마지막 캔들 시각 (형식: yyyy-MM-dd'T'HH:mm:ss'Z' 또는 yyyy-MM-dd HH:mm:ss)

    Returns:
        str: YAML 형식의 캔들스틱 데이터
    """
    if count > 200:
        count = 200
        await ctx_warning(ctx, "최대 200개의 캔들만 조회할 수 있습니다. count를 200으로 제한합니다.")

    params = {"market": market, "count": count}
    if to:
        params["to"] = to

    await ctx_info(ctx, f"{market} {interval} 캔들 데이터 조회 중...")

    try:
        client = get_public_client()
        candles_resource = client.candles

        if interval in MINUTE_UNITS:
            candles = await candles_resource.list_minutes(MINUTE_UNITS[interval], **params)
        else:
            method = getattr(candles_resource, CANDLE_METHODS[interval])
            candles = await method(**params)

        candle_dicts = cast(list[dict[str, Any]], to_serializable(candles))
        return format_candles_yaml(candle_dicts, market, interval)
    except Exception as e:
        error_message = format_api_error(e)
        await ctx_error(ctx, error_message)
        return f"error: {error_message}\n"
