# AI Trading Bot (Advanced)

A production-style AI trading bot starter for crypto and stock markets. It includes:

- real market APIs (Binance and Alpha Vantage)
- technical indicator feature engineering
- ML-based signal generation using logistic regression
- risk management and position sizing
- backtesting engine
- FastAPI endpoints for analysis and paper trading workflows

## Features

- Crypto market data via Binance REST API
- Stock market data via Alpha Vantage
- SMA, EMA, RSI, MACD, volatility, and Bollinger band features
- AI signal scoring with ML confidence
- Position sizing and stop-loss estimates
- Endpoints for analysis and backtesting

## Prerequisites

- Python 3.11+
- A Binance API key is optional for public market data
- An Alpha Vantage API key if you want stock data

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./trading.db
BINANCE_API_KEY=
BINANCE_API_SECRET=
ALPHA_VANTAGE_API_KEY=your_key_here
```

## Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Example requests

```bash
curl "http://localhost:8000/api/market/analyze?symbol=BTCUSDT&market=crypto&interval=1h&limit=250&account_balance=10000"
curl "http://localhost:8000/api/backtest?symbol=BTCUSDT&market=crypto&interval=1h&limit=250&initial_capital=10000"
```

## Project structure

```text
app/
  __init__.py
  config.py
  database.py
  models.py
  main.py
  services/
    feature_engineering.py
    market_data.py
    market_data_provider.py
    risk_management.py
    strategy_engine.py
    trading_service.py
requirements.txt
.env.example
README.md
```

## Notes

This is a strong base for a real trading platform, but should still be treated as a research and paper-trading prototype. For production usage, add authentication, persistence, broker integrations, logs, and monitoring.
