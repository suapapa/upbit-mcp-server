from upbit_client import format_api_error, get_public_client, to_serializable


async def get_orderbook(symbol: str) -> dict:
    """Get orderbook snapshot for a given symbol"""
    try:
        client = get_public_client()
        orderbooks = await client.orderbooks.list(markets=symbol)
        return to_serializable(orderbooks[0])
    except Exception as e:
        return {"error": format_api_error(e)}
