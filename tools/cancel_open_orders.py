from fastmcp import Context
from typing import Literal, Optional

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def cancel_open_orders(
    cancel_side: Literal["bid", "ask", "all"] = "all",
    count: int = 20,
    pairs: Optional[str] = None,
    excluded_pairs: Optional[str] = None,
    quote_currencies: Optional[str] = None,
    order_by: Literal["asc", "desc"] = "desc",
    ctx: Context = None,
) -> dict:
    """
    미체결 주문을 일괄 취소합니다.

    Args:
        cancel_side (str): 취소할 주문 방향 - all(전체), bid(매수), ask(매도)
        count (int): 취소할 최대 주문 수 (최대 300, 기본 20)
        pairs (str, optional): 취소 대상 마켓 (쉼표 구분, 최대 20개)
        excluded_pairs (str, optional): 제외할 마켓 (쉼표 구분, 최대 20개)
        quote_currencies (str, optional): 기준 통화 필터 (예: KRW)
        order_by (str): 정렬 순서 - desc(최신순), asc(오래된순)

    Returns:
        dict: 일괄 취소 결과
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}

    params = {
        "cancel_side": cancel_side,
        "count": count,
        "order_by": order_by,
    }
    if pairs:
        params["pairs"] = pairs
    if excluded_pairs:
        params["excluded_pairs"] = excluded_pairs
    if quote_currencies:
        params["quote_currencies"] = quote_currencies

    if ctx:
        ctx.info(f"미체결 주문 일괄 취소 중: side={cancel_side}, count={count}")

    try:
        client = get_authenticated_client()
        result = await client.orders.cancel_open(**params)
        return to_serializable(result)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return {"error": format_api_error(e)}
