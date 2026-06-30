from fastmcp import Context
from typing import Literal, Optional

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def get_deposits_withdrawals(
    currency: Optional[str] = None,
    txid: Optional[str] = None,
    transaction_type: Literal["deposit", "withdraw"] = "deposit",
    page: int = 1,
    limit: int = 100,
    ctx: Context = None,
) -> list[dict]:
    """
    업비트 계정의 입출금 내역을 조회합니다.

    Args:
        currency (str, optional): 통화 코드 (예: BTC)
        txid (str, optional): 거래 ID
        transaction_type (str): 거래 유형 - deposit(입금) 또는 withdraw(출금)
        page (int): 페이지 번호
        limit (int): 페이지당 결과 개수 (최대 100)

    Returns:
        list[dict]: 입출금 내역
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return [{"error": "API 키가 설정되지 않았습니다."}]

    params = {"page": page, "limit": limit}
    if currency:
        params["currency"] = currency
    if txid:
        params["txids"] = [txid]

    if ctx:
        ctx.info(f"{transaction_type} 내역 조회 중")

    try:
        client = get_authenticated_client()
        if transaction_type == "deposit":
            page_result = await client.deposits.list(**params)
        else:
            page_result = await client.withdraws.list(**params)
        return to_serializable(page_result.items)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return [{"error": format_api_error(e)}]
