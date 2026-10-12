from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from app.services.alerts import send_alert
from app.services.portfolio_service import PortfolioService
from app.services.trading_service import analyze_market, backtest_symbol

app = FastAPI(title="AI Trading Bot Advanced", version="2.1.0")
portfolio = PortfolioService(initial_cash=10000.0)


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
async def run_backtest(
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


@app.get("/api/portfolio")
def portfolio_status() -> dict:
    return portfolio.summary()


@app.post("/api/alerts/test")
async def test_alerts(webhook_url: str | None = None, message: str = "Test trading alert"):
    result = await send_alert(message=message, webhook_url=webhook_url, metadata={"service": "ai-trading-bot"})
    return result


@app.get("/api/dashboard/summary")
async def dashboard_summary(symbol: str = Query("BTCUSDT"), market: str = Query("crypto")):
    result = await analyze_market(symbol=symbol, market=market, interval="1h", limit=200, account_balance=10000)
    return {
        "symbol": symbol,
        "market": market,
        "signal": result["latest_signal"]["signal"],
        "confidence": result["latest_signal"]["confidence"],
        "price": result["latest_signal"]["price"],
        "risk": result["risk"],
    }
