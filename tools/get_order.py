from fastmcp import Context
from typing import Optional

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def get_order(
    uuid: Optional[str] = None,
    identifier: Optional[str] = None,
    ctx: Context = None,
) -> dict:
    """
    업비트에서 특정 주문의 정보를 조회합니다.

    Args:
        uuid (str, optional): 주문 UUID
        identifier (str, optional): 조회용 사용자 지정 값

    Returns:
        dict: 주문 정보
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}

    if not uuid and not identifier:
        if ctx:
            ctx.error("uuid 또는 identifier 중 하나는 필수입니다.")
        return {"error": "uuid 또는 identifier 중 하나는 필수입니다."}

    params = {}
    if uuid:
        params["uuid"] = uuid
    if identifier:
        params["identifier"] = identifier

    if ctx:
        ctx.info(f"주문 정보 조회 중: {uuid or identifier}")

    try:
        client = get_authenticated_client()
        order = await client.orders.retrieve(**params)
        return to_serializable(order)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return {"error": format_api_error(e)}
