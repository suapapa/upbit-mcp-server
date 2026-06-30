from fastmcp import Context
import numpy as np
from typing import Literal

from upbit_client import format_api_error, get_public_client, to_serializable

MINUTE_UNITS = {
    "minute30": 30,
    "minute60": 60,
    "minute240": 240,
}


async def technical_analysis(
    market: str,
    interval: Literal["minute30", "minute60", "minute240", "day"],
    ctx: Context = None,
) -> dict:
    """
    특정 마켓에 대한 기본적인 기술적 분석을 수행합니다.

    Args:
        market (str): 마켓 코드 (예: KRW-BTC)
        interval (str): 시간 간격 (minute30, minute60, minute240, day)

    Returns:
        dict: 기술적 분석 결과
    """
    if ctx:
        ctx.info(f"{market} {interval} 기술적 분석 수행 중...")

    try:
        client = get_public_client()
        params = {"market": market, "count": 100}

        if interval.startswith("minute"):
            candles = await client.candles.list_minutes(MINUTE_UNITS[interval], **params)
        else:
            candles = await client.candles.list_days(**params)

        candle_dicts = to_serializable(candles)

        closes = np.array([float(candle["trade_price"]) for candle in candle_dicts])
        highs = np.array([float(candle["high_price"]) for candle in candle_dicts])
        lows = np.array([float(candle["low_price"]) for candle in candle_dicts])
        volumes = np.array([float(candle["candle_acc_trade_volume"]) for candle in candle_dicts])

        closes = np.flip(closes)
        highs = np.flip(highs)
        lows = np.flip(lows)
        volumes = np.flip(volumes)

        sma5 = np.mean(closes[-5:]) if len(closes) >= 5 else None
        sma10 = np.mean(closes[-10:]) if len(closes) >= 10 else None
        sma20 = np.mean(closes[-20:]) if len(closes) >= 20 else None
        sma50 = np.mean(closes[-50:]) if len(closes) >= 50 else None

        if len(closes) >= 15:
            delta = np.diff(closes)
            gain = np.where(delta > 0, delta, 0)
            loss = np.where(delta < 0, -delta, 0)

            avg_gain = np.mean(gain[:14])
            avg_loss = np.mean(loss[:14])

            for i in range(14, len(delta)):
                avg_gain = (avg_gain * 13 + gain[i]) / 14
                avg_loss = (avg_loss * 13 + loss[i]) / 14

            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
        else:
            rsi = None

        if len(closes) >= 20:
            middle_band = np.mean(closes[-20:])
            std_dev = np.std(closes[-20:])
            upper_band = middle_band + (2 * std_dev)
            lower_band = middle_band - (2 * std_dev)
        else:
            middle_band = upper_band = lower_band = None

        if len(closes) >= 26:
            ema12 = np.mean(closes[-12:])
            ema26 = np.mean(closes[-26:])
            macd_line = ema12 - ema26

            if len(closes) >= 35:
                signal_line = np.mean(
                    [
                        ema12 - ema26
                        for ema12, ema26 in zip(
                            [np.mean(closes[i - 12 : i]) for i in range(len(closes) - 8, len(closes) + 1)],
                            [np.mean(closes[i - 26 : i]) for i in range(len(closes) - 8, len(closes) + 1)],
                        )
                    ]
                )
                macd_histogram = macd_line - signal_line
            else:
                signal_line = macd_histogram = None
        else:
            macd_line = signal_line = macd_histogram = None

        if len(closes) >= 14:
            low_14 = np.min(lows[-14:])
            high_14 = np.max(highs[-14:])

            if high_14 - low_14 > 0:
                k_percent = ((closes[-1] - low_14) / (high_14 - low_14)) * 100
            else:
                k_percent = 50

            if len(closes) >= 16:
                d_percent = np.mean(
                    [
                        (
                            (closes[-3] - np.min(lows[-16:-2]))
                            / (np.max(highs[-16:-2]) - np.min(lows[-16:-2]))
                        )
                        * 100,
                        (
                            (closes[-2] - np.min(lows[-15:-1]))
                            / (np.max(highs[-15:-1]) - np.min(lows[-15:-1]))
                        )
                        * 100,
                        k_percent,
                    ]
                )
            else:
                d_percent = None
        else:
            k_percent = d_percent = None

        avg_volume = np.mean(volumes)
        current_volume = volumes[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0

        pivots = {}
        if len(closes) >= 20:
            pivot_point = (highs[-1] + lows[-1] + closes[-1]) / 3
            r1 = 2 * pivot_point - lows[-1]
            r2 = pivot_point + (highs[-1] - lows[-1])
            s1 = 2 * pivot_point - highs[-1]
            s2 = pivot_point - (highs[-1] - lows[-1])

            pivots = {
                "pivot": pivot_point,
                "r1": r1,
                "r2": r2,
                "s1": s1,
                "s2": s2,
            }

        analysis_result = {}
        current_price = closes[-1]

        if sma5 and sma20:
            if sma5 > sma20:
                analysis_result["ma_signal"] = "상승 추세 (황금 교차)"
            elif sma5 < sma20:
                analysis_result["ma_signal"] = "하락 추세 (죽음의 교차)"
            else:
                analysis_result["ma_signal"] = "중립"

        if rsi is not None:
            if rsi > 70:
                analysis_result["rsi_signal"] = "과매수"
            elif rsi < 30:
                analysis_result["rsi_signal"] = "과매도"
            else:
                analysis_result["rsi_signal"] = "중립"

        if upper_band and lower_band:
            if current_price > upper_band:
                analysis_result["bb_signal"] = "과매수 (상단 돌파)"
            elif current_price < lower_band:
                analysis_result["bb_signal"] = "과매도 (하단 돌파)"
            else:
                analysis_result["bb_signal"] = "중립 (밴드 내)"

        if macd_line is not None and signal_line is not None:
            if macd_line > signal_line:
                analysis_result["macd_signal"] = "매수 신호"
            elif macd_line < signal_line:
                analysis_result["macd_signal"] = "매도 신호"
            else:
                analysis_result["macd_signal"] = "중립"

        if k_percent is not None and d_percent is not None:
            if k_percent > 80 and d_percent > 80:
                analysis_result["stoch_signal"] = "과매수"
            elif k_percent < 20 and d_percent < 20:
                analysis_result["stoch_signal"] = "과매도"
            elif k_percent > d_percent:
                analysis_result["stoch_signal"] = "상승 중"
            elif k_percent < d_percent:
                analysis_result["stoch_signal"] = "하락 중"
            else:
                analysis_result["stoch_signal"] = "중립"

        signals_count = len(analysis_result)
        buy_signals = sum(1 for signal in analysis_result.values() if "매수" in signal or "상승" in signal)
        sell_signals = sum(1 for signal in analysis_result.values() if "매도" in signal or "하락" in signal)
        oversold_signals = sum(1 for signal in analysis_result.values() if "과매도" in signal)
        overbought_signals = sum(1 for signal in analysis_result.values() if "과매수" in signal)

        if signals_count > 0:
            if buy_signals / signals_count > 0.6 or oversold_signals >= 2:
                analysis_result["overall_signal"] = "매수 고려"
            elif sell_signals / signals_count > 0.6 or overbought_signals >= 2:
                analysis_result["overall_signal"] = "매도 고려"
            else:
                analysis_result["overall_signal"] = "중립 관망"

        return {
            "market": market,
            "interval": interval,
            "current_price": current_price,
            "indicators": {
                "sma": {
                    "sma5": sma5,
                    "sma10": sma10,
                    "sma20": sma20,
                    "sma50": sma50,
                },
                "rsi": rsi,
                "bollinger_bands": {
                    "upper": upper_band,
                    "middle": middle_band,
                    "lower": lower_band,
                },
                "macd": {
                    "line": macd_line,
                    "signal": signal_line,
                    "histogram": macd_histogram,
                },
                "stochastic": {
                    "k": k_percent,
                    "d": d_percent,
                },
                "volume": {
                    "current": current_volume,
                    "average": avg_volume,
                    "ratio": volume_ratio,
                },
                "pivots": pivots,
            },
            "analysis": analysis_result,
        }

    except Exception as e:
        if ctx:
            ctx.error(format_api_error(e))
        return {"error": format_api_error(e)}
