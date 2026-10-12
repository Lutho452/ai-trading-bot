from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from app.services.trading_service import analyze_market, backtest_symbol

app = FastAPI(title="AI Trading Bot Advanced", version="2.0.0")


@app.get("/")
def root() -> dict:
    return {"message": "AI Trading Bot API is live"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ai-trading-bot"}


@app.get("/api/market/analyze")
async def market_analyze(
    symbol: str = Query(..., description="Ticker symbol such as BTCUSDT or AAPL"),
    market: str = Query(default="crypto", description="crypto|stock"),
    interval: str = Query(default="1h", description="Candlestick interval"),
    limit: int = Query(default=250, ge=50, le=1000),
    account_balance: float = Query(default=10000.0, ge=100.0),
):
    try:
        return await analyze_market(symbol=symbol, market=market, interval=interval, limit=limit, account_balance=account_balance)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/backtest")
async def backtest(
    symbol: str = Query(...),
    market: str = Query(default="crypto"),
    interval: str = Query(default="1h"),
    limit: int = Query(default=250, ge=50, le=1000),
    initial_capital: float = Query(default=10000.0, ge=100.0),
):
    try:
        return await backtest_symbol(symbol=symbol, market=market, interval=interval, limit=limit, initial_capital=initial_capital)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
