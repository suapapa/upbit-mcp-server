from fastmcp import Context
from typing import Literal, Optional

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def create_order(
    market: str,
    side: Literal["bid", "ask"],
    ord_type: Literal["limit", "price", "market"],
    volume: Optional[str] = None,
    price: Optional[str] = None,
    ctx: Context = None,
) -> dict:
    """
    업비트에 주문을 생성합니다.

    Args:
        market (str): 마켓 코드 (예: KRW-BTC)
        side (str): 주문 종류 - bid(매수) 또는 ask(매도)
        ord_type (str): 주문 타입 - limit(지정가), price(시장가 매수), market(시장가 매도)
        volume (str, optional): 주문량 (지정가, 시장가 매도 필수)
        price (str, optional): 주문 가격 (지정가 필수, 시장가 매수 필수)

    Returns:
        dict: 주문 결과
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}

    if ord_type == "limit" and (not volume or not price):
        if ctx:
            ctx.error("지정가 주문에는 volume과 price가 모두 필요합니다.")
        return {"error": "지정가 주문에는 volume과 price가 모두 필요합니다."}

    if ord_type == "price" and not price:
        if ctx:
            ctx.error("시장가 매수 주문에는 price가 필요합니다.")
        return {"error": "시장가 매수 주문에는 price가 필요합니다."}

    if ord_type == "market" and not volume:
        if ctx:
            ctx.error("시장가 매도 주문에는 volume이 필요합니다.")
        return {"error": "시장가 매도 주문에는 volume이 필요합니다."}

    params = {
        "market": market,
        "side": side,
        "ord_type": ord_type,
    }
    if volume:
        params["volume"] = volume
    if price:
        params["price"] = price

    if ctx:
        ctx.info(f"주문 생성 중: {market} {side} {ord_type}")

    try:
        client = get_authenticated_client()
        order = await client.orders.create(**params)
        return to_serializable(order)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return {"error": format_api_error(e)}
