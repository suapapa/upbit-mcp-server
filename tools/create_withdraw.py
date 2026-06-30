from fastmcp import Context
from typing import Literal, Optional

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def create_withdraw(
    currency: str,
    amount: str,
    address: Optional[str] = None,
    secondary_address: Optional[str] = None,
    transaction_type: Optional[str] = None,
    net_type: Optional[str] = None,
    two_factor_type: Optional[Literal["kakao", "naver", "hana"]] = None,
    ctx: Context = None,
) -> dict:
    """
    업비트에서 출금을 요청합니다.

    Args:
        currency (str): 통화 코드 (예: BTC)
        amount (str): 출금 수량
        address (str, optional): 출금 주소
        secondary_address (str, optional): 2차 출금 주소 (EOS, XRP 등에서 사용되는 Destination Tag, Memo)
        transaction_type (str, optional): 출금 유형
        net_type (str, optional): 디지털 자산 출금 네트워크 타입 (암호화폐 출금 시 필수)
        two_factor_type (str, optional): 원화 출금 2차 인증 방식 (kakao, naver, hana)

    Returns:
        dict: 출금 요청 결과
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}

    if currency.upper() == "KRW":
        if not two_factor_type:
            if ctx:
                ctx.error("원화 출금 시 two_factor_type(kakao, naver, hana)이 필요합니다.")
            return {"error": "원화 출금 시 two_factor_type(kakao, naver, hana)이 필요합니다."}
    else:
        if not address:
            if ctx:
                ctx.error("암호화폐 출금 시 address는 필수입니다.")
            return {"error": "암호화폐 출금 시 address는 필수입니다."}
        if not net_type:
            if ctx:
                ctx.error("암호화폐 출금 시 net_type은 필수입니다.")
            return {"error": "암호화폐 출금 시 net_type은 필수입니다."}

    if ctx:
        ctx.info(f"{currency} 출금 요청 중: {amount}")

    try:
        client = get_authenticated_client()

        if currency.upper() == "KRW":
            result = await client.withdraws.create_krw_withdrawal(
                amount=amount,
                two_factor_type=two_factor_type,
            )
        else:
            params = {
                "currency": currency,
                "amount": amount,
                "address": address,
                "net_type": net_type,
            }
            if secondary_address:
                params["secondary_address"] = secondary_address
            if transaction_type:
                params["transaction_type"] = transaction_type
            result = await client.withdraws.create_withdrawal(**params)

        return to_serializable(result)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return {"error": format_api_error(e)}
