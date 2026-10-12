# AI Trading Bot App

A lightweight AI-powered trading bot live built with Python and FastAPI. The app generates synthetic market data, computes technical indicators, scores BUY/SELL/HOLD signals, and runs a simple backtest.

## Features

- Synthetic OHLCV data generation
- Technical indicators: SMA, RSI, MACD, volatility
- AI-inspired signal engine
- Backtesting engine with equity curve
- REST API with FastAPI
- Optional Streamlit dashboard

## Stack

- Python 3.11+
- FastAPI
- Pandas / NumPy
- scikit-learn
- Streamlit

## Quick start

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the API:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Open the docs:
   - http://localhost:8000/docs

5. Optional dashboard:
   ```bash
   streamlit run dashboard.py
   ```

## API examples

```bash
curl http://localhost:8000/health
curl "http://localhost:8000/api/market/snapshot?symbol=BTCUSD&periods=200"
curl -X POST http://localhost:8000/api/backtest \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTCUSD","periods":200,"initial_capital":10000,"allocation":0.5}'
```

## Project layout

```text
app/
  __init__.py
  config.py
  data.py
  models.py
  strategies.py
  backtest.py
  main.py

dashboard.py
requirements.txt
README.md
.gitignore
```

## Notes

This is a starter project for learning and prototyping. It does not include brokerage integration or live execution.
