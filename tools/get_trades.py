from upbit_client import format_api_error, get_public_client, to_serializable


async def get_trades(symbol: str) -> list[dict]:
    """Get recent trade ticks for a symbol"""
    try:
        client = get_public_client()
        trades = await client.trades.list(market=symbol)
        return to_serializable(trades)
    except Exception as e:
        return [{"error": format_api_error(e)}]
