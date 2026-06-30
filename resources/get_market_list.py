from upbit_client import format_api_error, get_public_client, to_serializable


async def get_market_list() -> list[str]:
    """Get available trading pairs from Upbit"""
    try:
        client = get_public_client()
        markets = await client.trading_pairs.list()
        return [item["market"] for item in to_serializable(markets)]
    except Exception as e:
        return [{"error": format_api_error(e)}]
