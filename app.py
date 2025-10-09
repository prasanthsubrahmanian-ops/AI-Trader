import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import altair as alt
from datetime import datetime, timedelta

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="PRASANTH AI Trading Insights", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------- CUSTOM STYLE -----------------------
custom_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

body, .main, .block-container, .sidebar .sidebar-content {
    background-color: #000 !important;
    color: #fff !important;
}

.main-header {
    margin-top: 0rem;
    margin-bottom: 2rem;
    font-size: 2.5rem;
    font-weight: 700;
    color: #00ffcc;
    text-align: center;
    padding: 1rem 0;
    border-bottom: 2px solid #00ffcc;
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

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #111 !important;
    border-right: 1px solid #333;
}

section[data-testid="stSidebar"] > div {
    background-color: #111 !important;
}

section[data-testid="stSidebar"] .stRadio label {
    color: white !important;
}

section[data-testid="stSidebar"] .stSelectbox label {
    color: white !important;
}

section[data-testid="stSidebar"] .stSlider label {
    color: white !important;
}

@media (max-width: 768px) {
    .landing-box { padding: 1.5rem; }
    .main-header { font-size: 2rem; text-align: center; }
    .stDataFrame { font-size: 12px; }
    .stMetric { margin: 0.2rem; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------- CACHED FUNCTIONS -----------------------
@st.cache_data(ttl=300)
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

# ----------------------- MAIN HEADER AT TOP -----------------------
st.markdown('<div class="main-header">PRASANTH AI TRADING INSIGHTS</div>', unsafe_allow_html=True)

# ----------------------- STOCK SELECTION -----------------------
stocks = {
    "RELIANCE": "RELIANCE.NS", 
    "TCS": "TCS.NS", 
    "INFY": "INFY.NS", 
    "HDFC BANK": "HDFCBANK.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "AAPL": "AAPL",
    "TSLA": "TSLA"
}

# ----------------------- SIDEBAR NAVIGATION -----------------------
with st.sidebar:
    st.markdown("### 📊 Navigation")
    st.markdown("---")
    
    section = st.radio(
        "Choose Section",
        ("Home", "Research Reports", "Options Trading", "Chart Analysis", "AI Predictions"),
        key="nav_radio"
    )
    
    st.markdown("---")
    st.markdown("### 🔍 Stock Selection")
    
    stock_name = st.selectbox("Select Stock", list(stocks.keys()), key="stock_select")
    period = st.slider("Period (Days)", 10, 365, 60, key="period_slider")
    
    st.markdown("---")
    st.markdown("### ℹ️ Info")
    st.markdown("""
    <div style='color: #888; font-size: 0.9rem;'>
    Real-time market data and AI-powered trading insights. 
    Select a stock and navigate through different sections for detailed analysis.
    </div>
    """, unsafe_allow_html=True)

ticker = stocks[stock_name]

# ----------------------- HOME SECTION -----------------------
if section == "Home":
    st.subheader(f"📊 {stock_name} - Real-Time Market Data")
    
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
                
                current_price = float(df['Close'].iloc[-1])
                prev_price = float(df['Close'].iloc[-2])
                price_change_pct = ((current_price - prev_price) / prev_price) * 100
                
                with col1:
                    st.metric("Current Price", f"{current_price:.2f}", f"{price_change_pct:+.2f}%")
                
                with col2:
                    current_volume = int(df['Volume'].iloc[-1])
                    avg_volume = float(df['Volume'].iloc[-5:].mean())
                    volume_change_pct = ((current_volume - avg_volume) / avg_volume) * 100
                    st.metric("Volume", f"{current_volume:,}", f"{volume_change_pct:+.1f}%")
                
                with col3:
                    high_52w = float(df['High'].max())
                    st.metric("52W High", f"{high_52w:.2f}")
                
                with col4:
                    low_52w = float(df['Low'].min())
                    st.metric("52W Low", f"{low_52w:.2f}")
                
                # Price Chart with Indicators
                st.subheader(f"{stock_name} Price Chart")
                
                # Create a simple chart using Altair with proper data structure
                chart_data = df[['Date', 'Close', 'SMA20', 'SMA50', 'EMA20']].copy()
                
                # Create base chart
                base = alt.Chart(chart_data).encode(
                    x='Date:T'
                ).properties(
                    height=400
                )
                
                # Create individual lines
                close_line = base.mark_line(color='#00ffcc').encode(
                    y='Close:Q',
                    tooltip=['Date:T', 'Close:Q']
                )
                
                sma20_line = base.mark_line(color='#ffaa00', strokeDash=[5,5]).encode(
                    y='SMA20:Q',
                    tooltip=['Date:T', 'SMA20:Q']
                )
                
                sma50_line = base.mark_line(color='#ff00ff', strokeDash=[5,5]).encode(
                    y='SMA50:Q',
                    tooltip=['Date:T', 'SMA50:Q']
                )
                
                ema20_line = base.mark_line(color='#33cc33', strokeDash=[2,2]).encode(
                    y='EMA20:Q',
                    tooltip=['Date:T', 'EMA20:Q']
                )
                
                # Combine all lines
                chart = close_line + sma20_line + sma50_line + ema20_line
                st.altair_chart(chart, use_container_width=True)
                st.caption("🟢 Close | 🟡 SMA20 | 🟣 SMA50 | 🟢 EMA20")
                
                # OHLC Data
                st.subheader("OHLC Data")
                display_df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].tail(30).copy()
                display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
                st.dataframe(display_df, use_container_width=True)
                
                # Volume Chart
                st.subheader("Trading Volume")
                volume_chart = alt.Chart(df).mark_bar(color='#00ccff').encode(
                    x='Date:T',
                    y='Volume:Q',
                    tooltip=['Date:T', 'Volume:Q']
                ).properties(
                    height=300
                )
                st.altair_chart(volume_chart, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")

# ----------------------- RESEARCH REPORTS -----------------------
elif section == "Research Reports":
    st.markdown(
        '<div class="landing-box"><h2>📑 Research Reports</h2><p>Access AI-powered fundamental & technical analysis reports here.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Display current stock info
    try:
        df = get_stock_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**Current {stock_name} Price:** {current_price:.2f}")
    except:
        pass
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fundamental Analysis")
        st.metric("P/E Ratio", "22.5", "1.2")
        st.metric("EPS", "85.20", "5.0")
        st.metric("Market Cap", "12.5T", "2.3")
        
    with col2:
        st.subheader("Technical Ratings")
        st.metric("RSI Signal", "Neutral")
        st.metric("Moving Avg", "Bullish")
        st.metric("Volatility", "Medium")
    
    uploaded_file = st.file_uploader("Upload Research PDF", type="pdf")
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

# ----------------------- OPTIONS TRADING -----------------------
elif section == "Options Trading":
    st.markdown(
        '<div class="landing-box"><h2>💹 Options Trading</h2><p>Monitor open interest, volatility, and strategy payoffs.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Display current stock info
    try:
        df = get_stock_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**Current {stock_name} Price:** {current_price:.2f}")
    except:
        pass
    
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
                    calls_df = opt_chain.calls.head(8)[['strike', 'lastPrice', 'change', 'volume', 'openInterest']]
                    st.dataframe(calls_df)
                
                with col2:
                    st.write("**Puts**")
                    puts_df = opt_chain.puts.head(8)[['strike', 'lastPrice', 'change', 'volume', 'openInterest']]
                    st.dataframe(puts_df)
            else:
                st.info("Options data not available for this symbol")
        except Exception as e:
            st.info(f"Options data not available: {str(e)}")

# ----------------------- CHART ANALYSIS -----------------------
elif section == "Chart Analysis":
    st.markdown(
        '<div class="landing-box"><h2>📈 Chart Analysis</h2><p>Advanced technical analysis with multiple indicators.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Display current stock info
    try:
        df = get_stock_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**Current {stock_name} Price:** {current_price:.2f}")
    except:
        pass
    
    try:
        df = get_stock_data(ticker, period)
        if not df.empty:
            df.reset_index(inplace=True)
            
            st.subheader("Technical Indicators")
            
            col1, col2 = st.columns(2)
            with col1:
                show_rsi = st.checkbox("RSI", value=True)
                show_macd = st.checkbox("MACD", value=True)
            
            # RSI Calculation and Display
            if show_rsi:
                df['RSI'] = calculate_rsi(df['Close'])
                st.subheader("RSI (Relative Strength Index)")
                
                # Display RSI values
                current_rsi = df['RSI'].iloc[-1]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current RSI", f"{current_rsi:.2f}")
                with col2:
                    if current_rsi < 30:
                        st.metric("Signal", "OVERSOLD", delta="Buy Opportunity")
                    elif current_rsi > 70:
                        st.metric("Signal", "OVERBOUGHT", delta="Sell Opportunity")
                    else:
                        st.metric("Signal", "NEUTRAL")
                with col3:
                    st.metric("RSI Trend", "Up" if current_rsi > df['RSI'].iloc[-5] else "Down")
                
                # RSI chart using Altair
                rsi_chart = alt.Chart(df).mark_line(color='#ff6b6b').encode(
                    x='Date:T',
                    y=alt.Y('RSI:Q', scale=alt.Scale(domain=[0, 100])),
                    tooltip=['Date:T', 'RSI:Q']
                ).properties(height=300)
                
                # Add reference lines
                overbought = alt.Chart(pd.DataFrame({'y': [70]})).mark_rule(color='red', strokeDash=[5,5]).encode(y='y:Q')
                oversold = alt.Chart(pd.DataFrame({'y': [30]})).mark_rule(color='green', strokeDash=[5,5]).encode(y='y:Q')
                neutral = alt.Chart(pd.DataFrame({'y': [50]})).mark_rule(color='gray', strokeDash=[2,2]).encode(y='y:Q')
                
                st.altair_chart(rsi_chart + overbought + oversold + neutral, use_container_width=True)
                st.caption("RSI above 70: Overbought | RSI below 30: Oversold")
            
            # MACD Calculation and Display
            if show_macd:
                macd, signal, histogram = calculate_macd(df['Close'])
                st.subheader("MACD")
                
                # Display MACD values
                current_macd = macd.iloc[-1]
                current_signal = signal.iloc[-1]
                current_histogram = histogram.iloc[-1]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("MACD", f"{current_macd:.4f}")
                with col2:
                    st.metric("Signal", f"{current_signal:.4f}")
                with col3:
                    st.metric("Histogram", f"{current_histogram:.4f}")
                
                # MACD chart using Altair
                macd_data = pd.DataFrame({
                    'Date': df['Date'],
                    'MACD': macd.values,
                    'Signal': signal.values
                })
                
                macd_base = alt.Chart(macd_data).encode(x='Date:T')
                
                macd_line = macd_base.mark_line(color='#00ffcc').encode(
                    y='MACD:Q',
                    tooltip=['Date:T', 'MACD:Q']
                )
                
                signal_line = macd_base.mark_line(color='#ffaa00').encode(
                    y='Signal:Q',
                    tooltip=['Date:T', 'Signal:Q']
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
            
            current_price = float(df['Close'].iloc[-1])
            sma_20 = float(df['SMA20'].iloc[-1])
            sma_50 = float(df['SMA50'].iloc[-1])
            rsi = float(calculate_rsi(df['Close']).iloc[-1])
            
            # Simple AI Prediction Logic
            st.subheader(f"🎯 {stock_name} - AI Trading Signal")
            
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
            price_5d_ago = float(df['Close'].iloc[-5])
            price_change_5d = ((current_price - price_5d_ago) / price_5d_ago) * 100
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
                st.metric("Current Price", f"{current_price:.2f}")
            
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
                volatility = float(df['Close'].pct_change().std() * 100)
                st.metric("Volatility", f"{volatility:.1f}%")
            
            # Price Targets
            st.subheader("Price Targets")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if trend == "BULLISH":
                    target_1 = current_price * 1.05
                    target_2 = current_price * 1.10
                    st.metric("Target 1 (5%)", f"{target_1:.2f}")
                    st.metric("Target 2 (10%)", f"{target_2:.2f}")
                else:
                    target_1 = current_price * 0.95
                    target_2 = current_price * 0.90
                    st.metric("Support 1 (5%)", f"{target_1:.2f}")
                    st.metric("Support 2 (10%)", f"{target_2:.2f}")
            
            with col2:
                stop_loss = current_price * 0.97 if trend == "BULLISH" else current_price * 1.03
                st.metric("Stop Loss", f"{stop_loss:.2f}")
            
            with col3:
                risk_reward = "1:2" if trend == "BULLISH" else "1:1.5"
                st.metric("Risk/Reward", risk_reward)
                
        else:
            st.warning("Insufficient data for AI predictions")
            
    except Exception as e:
        st.error(f"Error generating predictions: {str(e)}")

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>PRASANTH AI TRADING INSIGHTS • Real-time Market Data</div>", unsafe_allow_html=True)