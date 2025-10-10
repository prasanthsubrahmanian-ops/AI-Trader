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

# ----------------------- CUSTOM STYLE -----------------------
custom_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Completely remove the default sidebar collapse buttons */
button[title="Hide sidebar"] {
    display: none !important;
}

button[title="Show sidebar"] {
    display: none !important;
}

body, .main, .block-container {
    background-color: #000 !important;
    color: #fff !important;
}

.main-header {
    margin-top: 0rem;
    margin-bottom: 1rem;
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
    border-right: 2px solid #00ffcc;
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

section[data-testid="stSidebar"] h3 {
    color: #00ffcc !important;
}

section[data-testid="stSidebar"] .stButton button {
    background-color: #00ffcc;
    color: #000;
    font-weight: bold;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background-color: #00e6b8;
}

/* Quick navigation buttons when sidebar is hidden */
.quick-nav {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.quick-nav button {
    background: #00ffcc;
    color: #000;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
}

.quick-nav button:hover {
    background: #00e6b8;
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

# ----------------------- SESSION STATE -----------------------
# Initialize session state
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True
if 'section' not in st.session_state:
    st.session_state.section = "Home"
if 'stock_name' not in st.session_state:
    st.session_state.stock_name = "RELIANCE"
if 'period' not in st.session_state:
    st.session_state.period = 60

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

# ----------------------- CUSTOM TOGGLE BUTTON -----------------------
# Create a custom toggle button using Streamlit components
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("☰", key="sidebar_toggle", help="Toggle Sidebar"):
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
        st.rerun()

# ----------------------- MAIN HEADER AT TOP -----------------------
st.markdown('<div class="main-header">PRASANTH AI TRADING INSIGHTS</div>', unsafe_allow_html=True)

# ----------------------- SIDEBAR NAVIGATION -----------------------
# Only show sidebar if it's supposed to be visible
if st.session_state.sidebar_visible:
    with st.sidebar:
        st.title("📊 PRASANTH AI")
        
        # Manual sidebar toggle button inside sidebar
        if st.button("📱 Close Sidebar"):
            st.session_state.sidebar_visible = False
            st.rerun()
        
        st.markdown("### 🧭 Navigation")
        section = st.radio(
            "Choose Section:",
            ["Home", "Research Reports", "Options Trading", "Chart Analysis", "AI Predictions"],
            key="nav_radio"
        )
        
        st.markdown("---")
        
        # Stock selection section
        st.markdown("### 🔍 Stock Selection")
        stock_name = st.selectbox("Select Stock:", list(stocks.keys()), key="stock_select")
        period = st.slider("Period (Days):", 10, 365, 60, key="period_slider")
        
        st.markdown("---")
        
        # Info section
        st.markdown("### ℹ️ About")
        st.info("""
        Real-time market data and 
        AI-powered trading insights.
        Select a stock and navigate 
        through sections for analysis.
        """)
        
        # Update session state with sidebar selections
        st.session_state.section = section
        st.session_state.stock_name = stock_name
        st.session_state.period = period

else:
    # If sidebar is hidden, show quick navigation buttons
    st.info("💡 Sidebar is hidden. Click the ☰ button in the top-left to show navigation.")
    
    # Quick navigation buttons
    st.markdown('<div class="quick-nav">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Home"):
            st.session_state.section = "Home"
            st.rerun()
    with col2:
        if st.button("📑 Research"):
            st.session_state.section = "Research Reports"
            st.rerun()
    with col3:
        if st.button("💹 Options"):
            st.session_state.section = "Options Trading"
            st.rerun()
    with col4:
        if st.button("📈 Charts"):
            st.session_state.section = "Chart Analysis"
            st.rerun()
    with col5:
        if st.button("🤖 AI"):
            st.session_state.section = "AI Predictions"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show current stock and allow quick change
    st.subheader("🔍 Quick Stock Selection")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_stock = st.selectbox("Select Stock:", list(stocks.keys()), 
                               index=list(stocks.keys()).index(st.session_state.stock_name),
                               key="quick_stock_select")
        if new_stock != st.session_state.stock_name:
            st.session_state.stock_name = new_stock
            st.rerun()
    
    with col2:
        new_period = st.slider("Period:", 10, 365, st.session_state.period, key="quick_period_slider")
        if new_period != st.session_state.period:
            st.session_state.period = new_period
            st.rerun()

# Use the values from session state
section = st.session_state.section
stock_name = st.session_state.stock_name
period = st.session_state.period

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

# ----------------------- OTHER SECTIONS -----------------------
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
    st.info("Options data feature will be available soon.")

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
    
    st.info("Advanced chart analysis features coming soon.")

elif section == "AI Predictions":
    st.markdown(
        '<div class="landing-box"><h2>🤖 AI Predictions</h2><p>AI-powered price predictions and trading signals.</p></div>',
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
    
    st.info("AI prediction models will be deployed soon.")

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>PRASANTH AI TRADING INSIGHTS • Real-time Market Data</div>", unsafe_allow_html=True)