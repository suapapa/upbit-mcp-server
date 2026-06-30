from fastmcp import Context

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def get_deposit_coin_address(
    currency: str,
    net_type: str,
    ctx: Context = None,
) -> dict:
    """
    특정 디지털 자산의 입금 주소를 조회합니다.

    Args:
        currency (str): 통화 코드 (예: BTC)
        net_type (str): 블록체인 네트워크 식별자 (예: BTC, ETH)

    Returns:
        dict: 입금 주소 정보
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}

    if ctx:
        ctx.info(f"입금 주소 조회 중: {currency} ({net_type})")

    try:
        client = get_authenticated_client()
        address = await client.deposits.retrieve_coin_address(currency=currency, net_type=net_type)
        return to_serializable(address)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return {"error": format_api_error(e)}
