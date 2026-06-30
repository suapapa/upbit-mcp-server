from fastmcp import Context

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def get_order_chance(
    market: str,
    ctx: Context = None,
) -> dict:
    """
    특정 마켓의 주문 가능 정보(수수료, 최소 주문 금액 등)를 조회합니다.

    Args:
        market (str): 마켓 코드 (예: KRW-BTC)

    Returns:
        dict: 주문 가능 정보
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}

    if ctx:
        ctx.info(f"주문 가능 정보 조회 중: {market}")

    try:
        client = get_authenticated_client()
        chance = await client.orders.retrieve_chance(market=market)
        return to_serializable(chance)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return {"error": format_api_error(e)}
