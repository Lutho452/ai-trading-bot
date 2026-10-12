from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from app.services.market_data import fetch_market_data
from app.services.risk_management import RiskManager
from app.services.strategy_engine import StrategyEngine


async def analyze_market(
    symbol: str,
    market: str = "crypto",
    interval: str = "1h",
    limit: int = 250,
    account_balance: float = 10000.0,
) -> Dict[str, Any]:
    data = await fetch_market_data(symbol=symbol, market=market, interval=interval, limit=limit)
    engine = StrategyEngine()
    engine.train(data)
    signal = engine.generate_signal(data, account_balance=account_balance)
    risk = RiskManager().get_position_size(
        account_balance=account_balance,
        signal=signal["signal"],
        price=signal["price"],
        confidence=signal["confidence"],
    )
    return {
        "symbol": symbol,
        "market": market,
        "interval": interval,
        "latest_signal": signal,
        "risk": risk,
        "data_points": len(data),
    }


async def backtest_symbol(
    symbol: str,
    market: str = "crypto",
    interval: str = "1h",
    limit: int = 250,
    initial_capital: float = 10000.0,
) -> Dict[str, Any]:
    data = await fetch_market_data(symbol=symbol, market=market, interval=interval, limit=limit)
    if data.empty:
        return {"signal": "HOLD", "equity_curve": [initial_capital], "total_return": 0.0}

    frame = data.copy()
    frame["signal"] = "HOLD"
    signal_engine = StrategyEngine()
    signal_engine.train(frame)

    cash = initial_capital
    position = 0.0
    equity_curve = [initial_capital]

    for idx in range(1, len(frame)):
        current_window = frame.iloc[: idx + 1]
        signal = signal_engine.generate_signal(current_window, account_balance=cash)
        current_price = float(frame.iloc[idx]["close"])

        if signal["signal"] == "BUY" and position == 0:
            position = (cash * 0.5) / current_price
            cash *= 0.5
        elif signal["signal"] == "SELL" and position > 0:
            cash += position * current_price
            position = 0.0

        current_value = cash + (position * current_price)
        equity_curve.append(float(current_value))

    final_value = equity_curve[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    return {
        "symbol": symbol,
        "initial_capital": initial_capital,
        "final_value": final_value,
        "total_return": round(float(total_return), 4),
        "equity_curve": [round(float(v), 2) for v in equity_curve],
    }
