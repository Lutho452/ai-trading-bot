import streamlit as st

from app.data import generate_market_data
from app.strategies import analyze_signal

st.set_page_config(page_title="AI Trading Bot", layout="wide")
st.title("AI Trading Bot Dashboard")

symbol = st.text_input("Symbol", value="BTCUSD")
periods = st.slider("Periods", min_value=100, max_value=500, value=250)

if st.button("Generate Signal"):
    data = generate_market_data(symbol=symbol, periods=periods)
    latest_signal = analyze_signal(data)

    st.subheader(f"Latest signal for {symbol}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Signal", latest_signal["signal"])
    col2.metric("Confidence", f"{latest_signal['confidence'] * 100:.1f}%")
    col3.metric("Price", f"${latest_signal['price']:.2f}")

    st.write("Reasons:")
    for reason in latest_signal["reasons"]:
        st.write("- " + reason)

    st.line_chart(data.set_index("timestamp")["close"])
