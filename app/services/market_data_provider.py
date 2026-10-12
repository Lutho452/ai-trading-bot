from __future__ import annotations

import pandas as pd

from app.services.market_data_provider import BinanceProvider, AlphaVantageProvider


async def fetch_market_data(symbol: str, market: str = "crypto", interval: str = "1h", limit: int = 200) -> pd.DataFrame:
    if market.lower() == "stock":
        provider = AlphaVantageProvider()
    else:
        provider = BinanceProvider()
    return await provider.get_ohlcv(symbol=symbol, interval=interval, limit=limit)
