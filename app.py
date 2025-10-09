import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import altair as alt
from datetime import datetime, timedelta

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

.metric-card {
    background-color: #1a1a1a;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #00ffcc;
    margin: 0.5rem 0;
}

@media (max-width: 768px) {
    .landing-box { padding: 1.5rem; }
    .header-text { font-size: 2rem; text-align: center; }
    .stDataFrame { font-size: 12px; }
    .stMetric { margin: 0.2rem; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------- CACHED FUNCTIONS -----------------------
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_data(ticker, period):
    return yf.download(ticker, period=f"{period}d")

def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

# ----------------------- SIDEBAR NAVIGATION -----------------------
st.sidebar.image("https://i.imgur.com/R6yR4hZ.png", use_container_width=True)
section = st.sidebar.radio(
    "Navigation",
    ("Home", "Research Reports", "Options Trading", "Chart Analysis", "AI Predictions")
)

# ----------------------- HEADER -----------------------
st.markdown('<div class="header-text">PRASANTH AI Trading Insights</div>', unsafe_allow_html=True)

# ----------------------- STOCK SELECTION -----------------------
stocks = {
    "TCS": "TCS.NS", 
    "RELIANCE": "RELIANCE.NS", 
    "INFY": "INFY.NS", 
    "HDFC BANK": "HDFCBANK.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "AAPL": "AAPL",
    "TSLA": "TSLA"
}

stock_name = st.selectbox("Select Stock", list(stocks.keys()))
period = st.slider("Period (Days)", 10, 365, 60)
ticker = stocks[stock_name]

# ----------------------- HOME SECTION -----------------------
if section == "Home":
    st.subheader("📊 Real-Time Market Data")
    
    with st.spinner(f"Fetching {stock_name} data..."):
        try:
            df = get_stock_data(ticker, period)
            if df.empty:
                st.error("No data available. Try again later or choose another stock.")
            else:
                df.reset_index(inplace=True)
                df["SMA20"] = df["Close"].rolling(20).mean()
                df["SMA50"] = df["Close"].rolling(50).mean()
                df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
                
                # Key Metrics
                st.subheader("📈 Key Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
                    st.metric("Daily Change", f"₹{df['Close'].iloc[-1]:.2f}", f"{price_change:+.2f}%")
                
                with col2:
                    volume_change = ((df['Volume'].iloc[-1] - df['Volume'].iloc[-5:].mean()) / df['Volume'].iloc[-5:].mean()) * 100
                    st.metric("Volume", f"{df['Volume'].iloc[-1]:,}", f"{volume_change:+.1f}%")
                
                with col3:
                    st.metric("52W High", f"₹{df['High'].max():.2f}")
                
                with col4:
                    st.metric("52W Low", f"₹{df['Low'].min():.2f}")
                
                # Price Chart with Indicators
                st.subheader(f"{stock_name} Price Chart")
                
                base_chart = alt.Chart(df).encode(x=alt.X("Date:T", title="Date"))
                
                price_line = base_chart.mark_line(color="#00ffcc").encode(
                    y=alt.Y("Close:Q", title="Price"),
                    tooltip=["Date:T", "Open", "High", "Low", "Close"]
                )
                
                sma20 = base_chart.mark_line(color="#ffaa00").encode(y="SMA20:Q")
                sma50 = base_chart.mark_line(color="#ff00ff").encode(y="SMA50:Q")
                ema20 = base_chart.mark_line(color="#33cc33").encode(y="EMA20:Q")
                
                st.altair_chart(price_line + sma20 + sma50 + ema20, use_container_width=True)
                st.caption("🟢 EMA20 | 🟡 SMA20 | 🟣 SMA50")
                
                # OHLC Data
                st.subheader("OHLC Data")
                st.dataframe(df[["Date", "Open", "High", "Low", "Close", "Volume"]].tail(30), use_container_width=True)
                
                # Volume Chart
                st.subheader("Trading Volume")
                volume_chart = alt.Chart(df).mark_bar(color="#00ccff").encode(
                    x="Date:T", 
                    y="Volume:Q",
                    tooltip=["Date:T", "Volume:Q"]
                ).interactive()
                st.altair_chart(volume_chart, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")

# ----------------------- RESEARCH REPORTS -----------------------
elif section == "Research Reports":
    st.markdown(
        '<div class="landing-box"><h2>📑 Research Reports</h2><p>Access AI-powered fundamental & technical analysis reports here.</p></div>',
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fundamental Analysis")
        st.metric("P/E Ratio", "22.5", "+1.2")
        st.metric("EPS", "₹85.20", "+5%")
        st.metric("Market Cap", "₹12.5T", "+2.3%")
        
    with col2:
        st.subheader("Technical Ratings")
        st.metric("RSI Signal", "Neutral", "-")
        st.metric("Moving Avg", "Bullish", "↑")
        st.metric("Volatility", "Medium", "-")
    
    uploaded_file = st.file_uploader("Upload Research PDF", type="pdf")
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

# ----------------------- OPTIONS TRADING -----------------------
elif section == "Options Trading":
    st.markdown(
        '<div class="landing-box"><h2>💹 Options Trading</h2><p>Monitor open interest, volatility, and strategy payoffs.</p></div>',
        unsafe_allow_html=True,
    )
    
    st.subheader("Options Chain")
    
    if st.button("Fetch Options Data"):
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options
            if expirations:
                selected_expiry = st.selectbox("Select Expiry", expirations[:4])
                opt_chain = stock.option_chain(selected_expiry)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Calls**")
                    st.dataframe(opt_chain.calls.head(8)[['strike', 'lastPrice', 'change', 'volume', 'openInterest']])
                
                with col2:
                    st.write("**Puts**")
                    st.dataframe(opt_chain.puts.head(8)[['strike', 'lastPrice', 'change', 'volume', 'openInterest']])
            else:
                st.info("Options data not available for this symbol")
        except Exception as e:
            st.info("Options data not available for this symbol")

# ----------------------- CHART ANALYSIS -----------------------
elif section == "Chart Analysis":
    st.markdown(
        '<div class="landing-box"><h2>📈 Chart Analysis</h2><p>Advanced technical analysis with multiple indicators.</p></div>',
        unsafe_allow_html=True,
    )
    
    try:
        df = get_stock_data(ticker, period)
        if not df.empty:
            df.reset_index(inplace=True)
            
            st.subheader("Technical Indicators")
            
            col1, col2 = st.columns(2)
            with col1:
                show_rsi = st.checkbox("RSI", value=True)
                show_macd = st.checkbox("MACD", value=True)
            with col2:
                show_bollinger = st.checkbox("Bollinger Bands")
                show_volume = st.checkbox("Volume", value=True)
            
            # RSI Calculation and Chart
            if show_rsi:
                df['RSI'] = calculate_rsi(df['Close'])
                st.subheader("RSI (Relative Strength Index)")
                
                rsi_chart = alt.Chart(df).mark_line(color="#ff6b6b").encode(
                    x='Date:T',
                    y=alt.Y('RSI:Q', scale=alt.Scale(domain=[0, 100])),
                    tooltip=['Date:T', 'RSI:Q']
                ).properties(height=300)
                
                # Add overbought/oversold lines
                overbought = alt.Chart(pd.DataFrame({'y': [70]})).mark_rule(color='red', strokeDash=[5,5]).encode(y='y:Q')
                oversold = alt.Chart(pd.DataFrame({'y': [30]})).mark_rule(color='green', strokeDash=[5,5]).encode(y='y:Q')
                middle = alt.Chart(pd.DataFrame({'y': [50]})).mark_rule(color='gray', strokeDash=[2,2]).encode(y='y:Q')
                
                st.altair_chart(rsi_chart + overbought + oversold + middle, use_container_width=True)
            
            # MACD Calculation and Chart
            if show_macd:
                macd, signal, histogram = calculate_macd(df['Close'])
                st.subheader("MACD")
                
                macd_df = df.copy()
                macd_df['MACD'] = macd
                macd_df['Signal'] = signal
                macd_df['Histogram'] = histogram
                
                macd_line = alt.Chart(macd_df).mark_line(color="#00ffcc").encode(
                    x='Date:T', y='MACD:Q'
                )
                signal_line = alt.Chart(macd_df).mark_line(color="#ffaa00").encode(
                    x='Date:T', y='Signal:Q'
                )
                
                st.altair_chart(macd_line + signal_line, use_container_width=True)
                
    except Exception as e:
        st.error(f"Error in chart analysis: {str(e)}")

# ----------------------- AI PREDICTIONS -----------------------
elif section == "AI Predictions":
    st.markdown(
        '<div class="landing-box"><h2>🤖 AI Predictions</h2><p>AI-powered price predictions and trading signals.</p></div>',
        unsafe_allow_html=True,
    )
    
    try:
        df = get_stock_data(ticker, period)
        if not df.empty and len(df) > 50:
            df.reset_index(inplace=True)
            df["SMA20"] = df["Close"].rolling(20).mean()
            df["SMA50"] = df["Close"].rolling(50).mean()
            
            current_price = df['Close'].iloc[-1]
            sma_20 = df['SMA20'].iloc[-1]
            sma_50 = df['SMA50'].iloc[-1]
            rsi = calculate_rsi(df['Close']).iloc[-1]
            
            # Simple AI Prediction Logic
            st.subheader("🎯 AI Trading Signal")
            
            prediction_score = 0
            
            # SMA Crossover Analysis
            if sma_20 > sma_50:
                prediction_score += 30
                trend = "BULLISH"
                trend_color = "#00ff00"
            else:
                prediction_score -= 20
                trend = "BEARISH" 
                trend_color = "#ff4444"
            
            # RSI Analysis
            if rsi < 30:
                prediction_score += 25  # Oversold - potential buy
            elif rsi > 70:
                prediction_score -= 25  # Overbought - potential sell
            
            # Price momentum
            price_change_5d = ((current_price - df['Close'].iloc[-5]) / df['Close'].iloc[-5]) * 100
            if price_change_5d > 2:
                prediction_score += 15
            elif price_change_5d < -2:
                prediction_score -= 15
            
            # Normalize score and generate prediction
            confidence = min(95, max(5, abs(prediction_score)))
            
            if prediction_score > 10:
                final_prediction = "STRONG BUY 🚀"
                final_color = "#00ff00"
            elif prediction_score > 0:
                final_prediction = "BUY 📈"
                final_color = "#88ff00"
            elif prediction_score > -10:
                final_prediction = "SELL 📉"
                final_color = "#ff8800"
            else:
                final_prediction = "STRONG SELL 🚨"
                final_color = "#ff4444"
            
            # Display Predictions
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div style='background: #1a1a1a; padding: 1.5rem; border-radius: 10px; border-left: 4px solid {final_color};'>
                    <h3 style='color: {final_color}; margin: 0;'>{final_prediction}</h3>
                    <p style='margin: 0.5rem 0 0 0; color: #ccc;'>AI Recommendation</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Confidence Score", f"{confidence:.1f}%")
            
            with col3:
                st.metric("Current Trend", trend)
            
            # Technical Factors
            st.subheader("Technical Factors")
            tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
            
            with tech_col1:
                st.metric("RSI", f"{rsi:.1f}")
            
            with tech_col2:
                sma_signal = "Bullish" if sma_20 > sma_50 else "Bearish"
                st.metric("SMA Signal", sma_signal)
            
            with tech_col3:
                st.metric("5D Change", f"{price_change_5d:+.1f}%")
            
            with tech_col4:
                volatility = df['Close'].pct_change().std() * 100
                st.metric("Volatility", f"{volatility:.1f}%")
            
            # Price Targets
            st.subheader("Price Targets")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if trend == "BULLISH":
                    target_1 = current_price * 1.05
                    target_2 = current_price * 1.10
                    st.metric("Target 1 (5%)", f"₹{target_1:.2f}")
                    st.metric("Target 2 (10%)", f"₹{target_2:.2f}")
                else:
                    target_1 = current_price * 0.95
                    target_2 = current_price * 0.90
                    st.metric("Support 1 (5%)", f"₹{target_1:.2f}")
                    st.metric("Support 2 (10%)", f"₹{target_2:.2f}")
            
            with col2:
                stop_loss = current_price * 0.97 if trend == "BULLISH" else current_price * 1.03
                st.metric("Stop Loss", f"₹{stop_loss:.2f}")
            
            with col3:
                risk_reward = "1:2" if trend == "BULLISH" else "1:1.5"
                st.metric("Risk/Reward", risk_reward)
                
        else:
            st.warning("Insufficient data for AI predictions")
            
    except Exception as e:
        st.error(f"Error generating predictions: {str(e)}")

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>PRASANTH AI Trading Insights • Real-time Market Data</div>", unsafe_allow_html=True)