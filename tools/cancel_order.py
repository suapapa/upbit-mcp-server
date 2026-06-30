from fastmcp import Context

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def cancel_order(
    uuid: str,
    ctx: Context = None,
) -> dict:
    """
    업비트에서 주문을 취소합니다.

    Args:
        uuid (str): 취소할 주문의 UUID

    Returns:
        dict: 취소 결과
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}

    if ctx:
        ctx.info(f"주문 취소 중: {uuid}")

    try:
        client = get_authenticated_client()
        order = await client.orders.cancel(uuid=uuid)
        return to_serializable(order)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return {"error": format_api_error(e)}
