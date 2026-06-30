from fastmcp import Context
from typing import Literal, Optional

from upbit_client import format_api_error, get_public_client, to_serializable

CANDLE_METHODS = {
    "day": "list_days",
    "week": "list_weeks",
    "month": "list_months",
}

MINUTE_UNITS = {
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
    ],
    count: int = 200,
    to: Optional[str] = None,
    ctx: Context = None,
) -> list[dict]:
    """
    업비트에서 캔들스틱 데이터를 조회합니다.

    Args:
        market (str): 마켓 코드 (예: KRW-BTC)
        interval (str): 시간 간격 (minute1~minute240, day, week, month)
        count (int): 캔들 개수 (최대 200)
        to (str, optional): 마지막 캔들 시각 (형식: yyyy-MM-dd'T'HH:mm:ss'Z' 또는 yyyy-MM-dd HH:mm:ss)

    Returns:
        list[dict]: 캔들스틱 데이터
    """
    if count > 200:
        count = 200
        if ctx:
            ctx.warning("최대 200개의 캔들만 조회할 수 있습니다. count를 200으로 제한합니다.")

    params = {"market": market, "count": count}
    if to:
        params["to"] = to

    if ctx:
        ctx.info(f"{market} {interval} 캔들 데이터 조회 중...")

    try:
        client = get_public_client()
        candles_resource = client.candles

        if interval in MINUTE_UNITS:
            candles = await candles_resource.list_minutes(MINUTE_UNITS[interval], **params)
        else:
            method = getattr(candles_resource, CANDLE_METHODS[interval])
            candles = await method(**params)

        return to_serializable(candles)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return [{"error": format_api_error(e)}]
