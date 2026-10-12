from __future__ import annotations

import numpy as np
import pandas as pd


def safe_rolling_mean(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=1).mean()


def calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def add_technical_features(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    if data.empty:
        return data

    data["returns"] = data["close"].pct_change().fillna(0)
    data["sma_10"] = safe_rolling_mean(data["close"], 10)
    data["sma_30"] = safe_rolling_mean(data["close"], 30)
    data["ema_12"] = data["close"].ewm(span=12, adjust=False).mean()
    data["ema_26"] = data["close"].ewm(span=26, adjust=False).mean()
    data["macd"] = data["ema_12"] - data["ema_26"]
    data["rsi_14"] = calculate_rsi(data["close"], 14)
    data["volatility"] = data["close"].pct_change().rolling(window=10, min_periods=1).std().fillna(0)
    rolling_mean = data["close"].rolling(window=20, min_periods=1).mean()
    rolling_std = data["close"].rolling(window=20, min_periods=1).std().fillna(0)
    data["bollinger_upper"] = rolling_mean + (rolling_std * 2)
    data["bollinger_lower"] = rolling_mean - (rolling_std * 2)
    data["bollinger_position"] = (data["close"] - data["bollinger_lower"]) / (data["bollinger_upper"] - data["bollinger_lower"]).replace(0, np.nan)
    data["bollinger_position"] = data["bollinger_position"].fillna(0.5)
    return data
