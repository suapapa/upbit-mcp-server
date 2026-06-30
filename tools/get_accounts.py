from fastmcp import Context

from config import UPBIT_ACCESS_KEY
from upbit_client import format_api_error, get_authenticated_client, to_serializable


async def get_accounts(ctx: Context = None) -> list[dict]:
    """
    업비트 계정의 잔고 정보를 조회합니다.

    Returns:
        list[dict]: 보유 중인 자산 목록
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return [{"error": "API 키가 설정되지 않았습니다."}]

    if ctx:
        ctx.info("계정 잔고 조회 중...")

    try:
        client = get_authenticated_client()
        accounts = await client.accounts.list()
        return to_serializable(accounts)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return [{"error": format_api_error(e)}]
