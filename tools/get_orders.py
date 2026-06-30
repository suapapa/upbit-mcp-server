from fastmcp import Context
from typing import Literal, Optional

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def get_orders(
    market: Optional[str] = None,
    state: Literal["wait", "done", "cancel"] = "wait",
    page: int = 1,
    limit: int = 100,
    ctx: Context = None,
) -> list[dict]:
    """
    업비트에서 주문 내역을 조회합니다.

    Args:
        market (str, optional): 마켓 코드 (예: KRW-BTC)
        state (str): 주문 상태 - wait(대기), done(완료), cancel(취소)
        page (int): 페이지 번호 (wait 상태에서만 사용)
        limit (int): 페이지당 주문 개수 (최대 100)

    Returns:
        list[dict]: 주문 내역
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return [{"error": "API 키가 설정되지 않았습니다."}]

    if ctx:
        ctx.info(f"주문 내역 조회 중: 상태={state}")

    try:
        client = get_authenticated_client()

        if state == "wait":
            params = {"page": page, "limit": limit}
            if market:
                params["market"] = market
            page_result = await client.orders.list_open(**params)
            return to_serializable(page_result.items)

        params = {"limit": limit, "state": state}
        if market:
            params["market"] = market
        if page > 1 and ctx:
            ctx.warning("done/cancel 상태에서는 page 파라미터가 지원되지 않아 무시됩니다.")

        orders = await client.orders.list_closed(**params)
        return to_serializable(orders)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return [{"error": format_api_error(e)}]
