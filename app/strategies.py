from __future__ import annotations

from typing import Dict, List

import pandas as pd


def analyze_signal(df: pd.DataFrame) -> Dict[str, object]:
    """Generate an AI-style signal based on key technical indicators."""
    latest = df.iloc[-1]
    score = 0.0
    reasons: List[str] = []

    if latest["sma_10"] > latest["sma_30"]:
        score += 1.5
        reasons.append("Short-term trend above long-term trend")
    elif latest["sma_10"] < latest["sma_30"]:
        score -= 1.5
        reasons.append("Short-term trend below long-term trend")

    if latest["rsi_14"] < 30:
        score += 1.2
        reasons.append("RSI indicates oversold conditions")
    elif latest["rsi_14"] > 70:
        score -= 1.2
        reasons.append("RSI indicates overbought conditions")

    if latest["macd"] > 0:
        score += 0.8
        reasons.append("MACD is positive")
    elif latest["macd"] < 0:
        score -= 0.8
        reasons.append("MACD is negative")

    if latest["volatility"] > 0.02:
        score -= 0.5
        reasons.append("Volatility is elevated")

    if score >= 1.0:
        signal = "BUY"
    elif score <= -1.0:
        signal = "SELL"
    else:
        signal = "HOLD"

    confidence = min(max(abs(score) / 4.0, 0.1), 0.95)

    return {
        "symbol": latest.get("symbol", "UNKNOWN"),
        "price": float(latest["close"]),
        "signal": signal,
        "confidence": round(float(confidence), 4),
        "score": round(float(score), 4),
        "reasons": reasons,
    }


def build_strategy_summary(df: pd.DataFrame) -> pd.DataFrame:
    latest = df.tail(1).copy()
    return latest[["symbol", "close", "sma_10", "sma_30", "rsi_14", "macd", "volatility"]]
