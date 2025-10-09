import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import altair as alt

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide")

# ----------------------- CUSTOM STYLE -----------------------
custom_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-1v3fvcr.egzxvld0 {visibility: hidden;}  /* user profile icon */

body, .main, .block-container, .sidebar .sidebar-content {
    background-color: #000 !important;
    color: #fff !important;
}

.header-text {
    margin-top: 2rem;
    margin-bottom: 2rem;
    font-size: 2.5rem;
    font-weight: 700;
    color: #00ffcc;
    text-align: left;
}

.landing-box {
    background-color: #111;
    padding: 2rem 2.5rem;
    border-radius: 12px;
    margin: 1.5rem 0;
    box-shadow: 0 4px 24px rgba(255, 255, 255, 0.1);
}

h2, h3, h4, p, label, .stRadio > label {
    color: #fff !important;
}

div[data-testid="stDataFrame"] {
    background-color: #222 !important;
    color: #fff !important;
}

@media (max-width: 768px) {
    .landing-box { padding: 1.5rem; }
    .header-text { font-size: 2rem; text-align: center; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------- SIDEBAR NAVIGATION -----------------------
st.sidebar.image("https://i.imgur.com/R6yR4hZ.png", use_container_width=True)
section = st.sidebar.radio(
    "Navigation",
    ("Home", "Research Reports", "Options Trading", "Chart Analysis", "AI Predictions")
)

# ----------------------- HEADER -----------------------
st.markdown('<div class="header-text">PRASANTH AI Trading Insights</div>', unsafe_allow_html=True)

# ----------------------- HOME SECTION -----------------------
if section == "Home":
    st.subheader("📊 Real-Time Market Data")

    stock_name = st.selectbox("Select Stock", ["TCS", "RELIANCE", "INFY", "NIFTY"])
    period = st.slider("Period (Days)", 10, 180, 60)

    symbol_map = {"TCS": "TCS.NS", "RELIANCE": "RELIANCE.NS", "INFY": "INFY.NS", "NIFTY": "^NSEI"}
    ticker = symbol_map[stock_name]

    with st.spinner(f"Fetching {stock_name} data..."):
        df = yf.download(ticker, period=f"{period}d", interval="1d")

    if df.empty:
        st.error("No data available. Try again later or choose another stock.")
    else:
        df.reset_index(inplace=True)
        df["SMA20"] = df["Close"].rolling(20).mean()
        df["SMA50"] = df["Close"].rolling(50).mean()
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

        st.subheader(f"{stock_name} Price Chart")

        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("Close:Q", title="Closing Price"),
                color=alt.value("#00ffcc"),
                tooltip=["Date:T", "Open", "High", "Low", "Close"]
            )
            .interactive()
        )

        sma20 = alt.Chart(df).mark_line(color="#ffaa00").encode(x="Date:T", y="SMA20:Q")
        sma50 = alt.Chart(df).mark_line(color="#ff00ff").encode(x="Date:T", y="SMA50:Q")
        ema20 = alt.Chart(df).mark_line(color="#33cc33").encode(x="Date:T", y="EMA20:Q")

        st.altair_chart(chart + sma20 + sma50 + ema20, use_container_width=True)

        st.caption("🟢 EMA20 | 🟡 SMA20 | 🟣 SMA50")

        st.subheader("OHLC Data")
        st.dataframe(df[["Date", "Open", "High", "Low", "Close", "Volume"]].tail(30), use_container_width=True)

        st.subheader("Trading Volume")
        volume_chart = (
            alt.Chart(df)
            .mark_bar(color="#00ccff")
            .encode(x="Date:T", y="Volume:Q")
            .interactive()
        )
        st.altair_chart(volume_chart, use_container_width=True)

# ----------------------- RESEARCH REPORTS -----------------------
elif section == "Research Reports":
    st.markdown(
        '<div class="landing-box"><h2>📑 Research Reports</h2><p>Access AI-powered fundamental & technical analysis reports here. Upload or link your custom PDFs and analytics dashboards.</p></div>',
        unsafe_allow_html=True,
    )

# ----------------------- OPTIONS TRADING -----------------------
elif section == "Options Trading":
    st.markdown(
        '<div class="landing-box"><h2>💹 Options Trading</h2><p>Monitor open interest, volatility, and strategy payoffs. Add your strategy builder or analytics module here.</p></div>',
        unsafe_allow_html=True,
    )

# ----------------------- CHART ANALYSIS -----------------------
elif section == "Chart Analysis":
    st.markdown(
        '<div class="landing-box"><h2>📈 Chart Analysis</h2><p>View advanced candlestick charts, RSI, MACD, and Bollinger Bands here. (Coming soon: Interactive charting tools.)</p></div>',
        unsafe_allow_html=True,
    )

# ----------------------- AI PREDICTIONS -----------------------
elif section == "AI Predictions":
    st.markdown(
        '<div class="landing-box"><h2>🤖 AI Predictions</h2><p>AI models will generate directional predictions, confidence scores, and trade signals here. Plug in your ML model APIs.</p></div>',
        unsafe_allow_html=True,
    )
