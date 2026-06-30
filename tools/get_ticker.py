from upbit_client import format_api_error, get_public_client, to_serializable


async def get_ticker(symbol: str) -> dict:
    """Get the latest ticker data from Upbit"""
    try:
        client = get_public_client()
        tickers = await client.tickers.list_by_trading_pairs(markets=symbol)
        return to_serializable(tickers[0])
    except Exception as e:
        return {"error": format_api_error(e)}
