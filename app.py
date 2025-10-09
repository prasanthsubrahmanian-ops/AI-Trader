import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

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

    # Plot chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'], high=data['High'],
        low=data['Low'], close=data['Close'],
        name='Market Data'
    ))
    fig.update_layout(title=f"{ticker} Price Chart", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # Calculate indicators
    data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()

    # RSI Calculation (Fixed)
    delta = data['Close'].diff()
    gain = delta.apply(lambda x: x if x > 0 else 0)
    loss = delta.apply(lambda x: abs(x) if x < 0 else 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    data['RSI'] = 100 - (100 / (1 + (avg_gain / avg_loss)))

    # Technical indicators chart
    st.subheader("📈 Technical Indicators")
    st.line_chart(data[['Close', 'EMA20', 'EMA50']])

    # RSI chart
    st.subheader("RSI (Relative Strength Index)")
    st.line_chart(data['RSI'])

    # Simple AI comment (rule-based for now)
    latest_rsi = data['RSI'].iloc[-1]
    if latest_rsi > 70:
        ai_comment = "⚠ The RSI suggests the stock may be *overbought*. Caution advised."
    elif latest_rsi < 30:
        ai_comment = "💡 The RSI suggests the stock may be *oversold*. It could rebound soon."
    else:
        ai_comment = "📊 The RSI indicates a *neutral* zone. Watch for breakout signals."

    st.markdown(f"### 🤖 AI Insight: {ai_comment}")

    # Show raw data
    with st.expander("View Raw Data"):
        st.dataframe(data.tail())


