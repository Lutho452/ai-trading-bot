from __future__ import annotations

from typing import Any

import httpx
import pandas as pd

from app.config import settings


class MarketDataProvider:
    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 200) -> pd.DataFrame:
        raise NotImplementedError


class BinanceProvider(MarketDataProvider):
    BASE_URL = "https://api.binance.com/api/v3"

    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 200) -> pd.DataFrame:
        market_symbol = symbol.upper().replace("-", "")
        if not market_symbol.endswith(("USDT", "USD")):
            market_symbol = f"{market_symbol}USDT"

        params = {"symbol": market_symbol, "interval": interval, "limit": limit}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/klines", params=params)
            response.raise_for_status()

        payload = response.json()
        columns = [
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "trade_count",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ]
        frame = pd.DataFrame(payload, columns=columns)
        if frame.empty:
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

        frame["timestamp"] = pd.to_datetime(frame["open_time"], unit="ms")
        frame = frame[["timestamp", "open", "high", "low", "close", "volume"]].astype({
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": float,
        })
        return frame.reset_index(drop=True)


class AlphaVantageProvider(MarketDataProvider):
    BASE_URL = "https://www.alphavantage.co/query"

    async def get_ohlcv(self, symbol: str, interval: str = "60min", limit: int = 200) -> pd.DataFrame:
        api_key = settings.ALPHA_VANTAGE_API_KEY
        if not api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY is not set")

        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol.upper(),
            "interval": interval,
            "outputsize": "compact",
            "apikey": api_key,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()

        payload = response.json()
        series_key = next((key for key in payload if "Time Series" in key), None)
        if not series_key:
            raise ValueError(f"Invalid Alpha Vantage response: {payload}")

        raw = payload[series_key]
        frame = pd.DataFrame.from_dict(raw, orient="index")
        frame = frame.rename(columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume",
        })
        frame = frame[["open", "high", "low", "close", "volume"]].astype(float)
        frame["timestamp"] = pd.to_datetime(frame.index)
        return frame.tail(limit).reset_index(drop=True)
