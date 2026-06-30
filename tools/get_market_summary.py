from fastmcp import Context

from config import MAJOR_COINS, create_error_response
from upbit_client import format_api_error, get_public_client, to_serializable


async def get_market_summary(ctx: Context = None) -> dict:
    """
    주요 암호화폐 시장의 요약 정보를 제공합니다.

    Returns:
        dict: 주요 암호화폐 시장 요약 정보
    """
    try:
        client = get_public_client()

        markets = await client.trading_pairs.list()
        krw_markets = [market for market in markets if market.market.startswith("KRW-")]

        all_tickers = await client.tickers.list_by_quote_currencies(quote_currencies="KRW")
        ticker_dicts = to_serializable(all_tickers)

        major_coin_info = [ticker for ticker in ticker_dicts if ticker["market"] in MAJOR_COINS]

        volume_sorted = sorted(
            [ticker for ticker in ticker_dicts if ticker["market"] not in MAJOR_COINS],
            key=lambda x: x["acc_trade_price_24h"],
            reverse=True,
        )
        top_volume_coins = volume_sorted[:5]

        price_change_sorted = sorted(ticker_dicts, key=lambda x: x["signed_change_rate"], reverse=True)
        top_gainers = price_change_sorted[:5]
        top_losers = price_change_sorted[-5:]

        return {
            "timestamp": ticker_dicts[0]["timestamp"] if ticker_dicts else None,
            "major_coins": major_coin_info,
            "top_volume": top_volume_coins,
            "top_gainers": top_gainers,
            "top_losers": top_losers,
            "krw_market_count": len(krw_markets),
        }
    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return create_error_response(format_api_error(e))
