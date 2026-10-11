from __future__ import annotations

import numpy as np
import pandas as pd

from app.config import DEFAULT_PERIODS, DEFAULT_SYMBOL


def calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def generate_market_data(symbol: str = DEFAULT_SYMBOL, periods: int = DEFAULT_PERIODS) -> pd.DataFrame:
    """Create synthetic OHLCV data with indicators."""
    if periods <= 0:
        raise ValueError("Periods must be greater than zero")

    rng = np.random.default_rng(42)
    base_price = 100.0
    trend = np.linspace(0, 30, periods)
    noise = rng.normal(0, 1.4, periods)
    closes = base_price + trend + noise
    closes = np.maximum(closes, 10)

    opens = np.roll(closes, 1)
    opens[0] = base_price

    highs = np.maximum(opens, closes) + rng.uniform(0.5, 3.5, periods)
    lows = np.minimum(opens, closes) - rng.uniform(0.5, 3.5, periods)
    volumes = rng.integers(500, 5000, periods)
    timestamps = pd.date_range(end=pd.Timestamp.utcnow(), periods=periods, freq="h")

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "symbol": symbol,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
        }
    )

    df["returns"] = df["close"].pct_change().fillna(0)
    df["sma_10"] = df["close"].rolling(window=10).mean()
    df["sma_30"] = df["close"].rolling(window=30).mean()
    df["volatility"] = df["close"].pct_change().rolling(window=10).std().fillna(0)
    df["rsi_14"] = calculate_rsi(df["close"], window=14)
    df["macd"] = df["close"].ewm(span=12, adjust=False).mean() - df["close"].ewm(span=26, adjust=False).mean()
    return df
