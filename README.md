import streamlit as st

from app.services.market_data import fetch_market_data
from app.services.strategy_engine import StrategyEngine

st.set_page_config(page_title="AI Trading Bot", layout="wide")

st.title("AI Trading Bot Dashboard")

symbol = st.text_input("Symbol", value="BTCUSDT")
market = st.selectbox("Market", ["crypto", "stock"])
interval = st.selectbox("Interval", ["1m", "5m", "15m", "1h", "4h", "1d"])
limit = st.slider("Candles", min_value=50, max_value=500, value=200)

if st.button("Analyze market"):
    try:
        data = st.session_state.get("market_data")
        if data is None:
            data = __import__("asyncio").run(fetch_market_data(symbol=symbol, market=market, interval=interval, limit=limit))
            st.session_state["market_data"] = data

        engine = StrategyEngine()
        engine.train(data)
        signal = engine.generate_signal(data)

        st.subheader(f"Signal for {symbol}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Signal", signal["signal"])
        col2.metric("Confidence", f"{signal['confidence'] * 100:.1f}%")
        col3.metric("Price", f"${signal['price']:.2f}")

        st.write("Reasons:")
        for reason in signal["reasons"]:
            st.write(f"- {reason}")

        st.line_chart(data.set_index("timestamp")["close"])
    except Exception as exc:
        st.error(f"Unable to fetch data: {exc}")

st.sidebar.header("Controls")
st.sidebar.caption("AI trading dashboard for research and paper trading")
