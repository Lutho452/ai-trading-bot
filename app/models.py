from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class MarketRequest(BaseModel):
    symbol: str = "BTCUSD"
    periods: int = Field(default=200, ge=50, le=5000)


class BacktestRequest(MarketRequest):
    initial_capital: float = Field(default=10000.0, gt=0)
    allocation: float = Field(default=0.5, gt=0, le=1)


class SignalResponse(BaseModel):
    symbol: str
    price: float
    signal: str
    confidence: float
    score: float
    reasons: List[str]


class BacktestSummary(BaseModel):
    symbol: str
    initial_capital: float
    final_value: float
    total_return_pct: float
    max_drawdown_pct: float
    trades: int
    signal_history: List[str]
    equity_curve: List[float]


class HealthResponse(BaseModel):
    status: str = "ok"
    app: str = "ai-trading-bot"
