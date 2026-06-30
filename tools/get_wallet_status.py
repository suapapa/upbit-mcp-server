from fastmcp import Context

from upbit_client import format_api_error, get_public_client, to_serializable


async def get_wallet_status(ctx: Context = None) -> list[dict]:
    """
    디지털 자산별 지갑 점검(입출금 가능) 상태를 조회합니다.

    Returns:
        list[dict]: 지갑 상태 목록
    """
    if ctx:
        ctx.info("지갑 상태 조회 중...")

    try:
        client = get_public_client()
        status = await client.wallet_status.list()
        return to_serializable(status)
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return [{"error": format_api_error(e)}]
