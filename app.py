import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

# Page config
st.set_page_config(page_title="AI Trading Dashboard", layout="wide")

st.title("🤖 AI Trading Dashboard")
st.markdown("Analyze stocks, visualize trends, and get simple AI insights.")

# Sidebar inputs
st.sidebar.header("📊 Select Stock")
ticker = st.sidebar.text_input("Enter stock symbol (e.g. TCS.NS, INFY.NS, RELIANCE.NS):", "TCS.NS")
period = st.sidebar.selectbox("Select Time Period:", ["1mo", "3mo", "6mo", "1y", "2y"])
interval = st.sidebar.selectbox("Select Interval:", ["1d", "1wk", "1mo"])

# Fetch data
data = yf.download(ticker, period=period, interval=interval)

if data.empty:
    st.error("No data found. Please check the symbol.")
else:
    st.success(f"Showing {ticker} data")

    # Candlestick chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'], high=data['High'],
        low=data['Low'], close=data['Close'],
        name='Market Data'
    ))
    fig.update_layout(title=f"{ticker} Price Chart", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # ---- Calculate Indicators ----
    data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()  

    # RSI calculation (clean version)
    gain = data['Close'].diff().apply(lambda x: np.where(x > 0, x, 0))
    loss = data['Close'].diff().apply(lambda x: np.where(x < 0, abs(x), 0))
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # ---- Technical Indicators ----
    st.subheader("📈 Technical Indicators")
    st.line_chart(data[['Close', 'EMA20', 'EMA50']])

    # ---- RSI Chart ----
    st.subheader("RSI (Relative Strength Index)")
    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
    rsi_fig.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="Overbought (70)")
    rsi_fig.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="Oversold (30)")
    rsi_fig.update_layout(title="RSI (14-period)", yaxis_title="RSI Value", xaxis_title="Date")
    st.plotly_chart(rsi_fig, use_container_width=True)

    # ---- Simple AI Insight ----
    latest_rsi = data['RSI'].iloc[-1]
    if latest_rsi > 70:
        ai_comment = "⚠ The RSI suggests the stock may be *overbought*. Caution advised."
    elif latest_rsi < 30:
        ai_comment = "💡 The RSI suggests the stock may be *oversold*. It could rebound soon."
    else:
        ai_comment = "📊 The RSI indicates a *neutral* zone. Watch for breakout signals."

    st.markdown(f"### 🤖 AI Insight: {ai_comment}")

    # ---- Show Raw Data ----
    with st.expander("View Raw Data"):
        st.dataframe(data.tail()
