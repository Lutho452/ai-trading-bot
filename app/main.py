from __future__ import annotations

from fastapi import FastAPI, Query

from app.backtest import BacktestEngine
from app.data import generate_market_data
from app.models import BacktestRequest, BacktestSummary, HealthResponse, MarketRequest, SignalResponse
from app.strategies import analyze_signal

app = FastAPI(title="AI Trading Bot", version="1.0.0")


@app.get("/", tags=["meta"])
def home() -> dict:
    return {"message": "AI Trading Bot API is running"}


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", app="ai-trading-bot")


@app.get("/api/market/snapshot", tags=["market"])
def market_snapshot(
    symbol: str = Query(default="BTCUSD", description="Ticker symbol"),
    periods: int = Query(default=200, ge=50, le=5000),
) -> dict:
    data = generate_market_data(symbol=symbol, periods=periods)
    latest = data.iloc[-1].to_dict()
    return {
        "symbol": symbol,
        "close": float(latest["close"]),
        "sma_10": float(latest["sma_10"]),
        "sma_30": float(latest["sma_30"]),
        "rsi_14": float(latest["rsi_14"]),
        "macd": float(latest["macd"]),
        "volatility": float(latest["volatility"]),
    }


@app.post("/api/strategy/signal", response_model=SignalResponse, tags=["strategy"])
def strategy_signal(request: MarketRequest) -> SignalResponse:
    data = generate_market_data(symbol=request.symbol, periods=request.periods)
    signal = analyze_signal(data)
    return SignalResponse(**signal)


@app.post("/api/backtest", response_model=BacktestSummary, tags=["backtest"])
def run_backtest(request: BacktestRequest) -> BacktestSummary:
    data = generate_market_data(symbol=request.symbol, periods=request.periods)
    engine = BacktestEngine(data, initial_capital=request.initial_capital, allocation=request.allocation)
    result = engine.run()
    return BacktestSummary(
        symbol=result["symbol"],
        initial_capital=result["initial_capital"],
        final_value=result["final_value"],
        total_return_pct=result["total_return_pct"],
        max_drawdown_pct=result["max_drawdown_pct"],
        trades=result["trades"],
        signal_history=result["signal_history"],
        equity_curve=result["equity_curve"],
    )
