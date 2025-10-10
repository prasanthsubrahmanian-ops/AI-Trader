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
    initial_sidebar_state="collapsed"
)

# ----------------------- CUSTOM STYLE -----------------------
custom_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hide the default sidebar completely */
section[data-testid="stSidebar"] {
    display: none !important;
}

button[title="Hide sidebar"] {
    display: none !important;
}

button[title="Show sidebar"] {
    display: none !important;
}

body, .main, .block-container {
    background-color: #000 !important;
    color: #fff !important;
    padding-top: 80px !important;
}

/* Custom Navigation Bar */
.custom-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #111;
    padding: 1rem 2rem;
    border-bottom: 2px solid #00ffcc;
    z-index: 9999;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 20px rgba(0, 255, 204, 0.2);
}

.nav-brand {
    font-size: 1.8rem;
    font-weight: 700;
    color: #00ffcc;
    margin: 0;
}

.nav-section {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.nav-button {
    background: transparent;
    border: 2px solid #00ffcc;
    color: #00ffcc;
    padding: 0.5rem 1.5rem;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.nav-button:hover {
    background-color: #00ffcc;
    color: #000;
    transform: translateY(-2px);
}

.nav-button.active {
    background-color: #00ffcc;
    color: #000;
}

.stock-selector {
    display: flex;
    gap: 1rem;
    align-items: center;
    background: #1a1a1a;
    padding: 0.8rem 1.5rem;
    border-radius: 25px;
    border: 1px solid #333;
}

.stock-selector select {
    background: #000;
    color: #fff;
    border: 1px solid #00ffcc;
    border-radius: 20px;
    padding: 0.3rem 1rem;
}

.period-display {
    color: #00ffcc;
    font-size: 0.9rem;
    min-width: 80px;
}

.main-header {
    margin-top: 2rem;
    margin-bottom: 2rem;
    font-size: 2.5rem;
    font-weight: 700;
    color: #00ffcc;
    text-align: center;
    padding: 1rem 0;
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

/* Hide Streamlit form elements */
.stForm {
    border: none !important;
}

.stForm > div {
    background: transparent !important;
}

@media (max-width: 768px) {
    .custom-navbar {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }
    
    .nav-section {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .stock-selector {
        flex-wrap: wrap;
    }
    
    .landing-box { padding: 1.5rem; }
    .main-header { font-size: 2rem; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------- SESSION STATE -----------------------
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Home"
if 'stock_name' not in st.session_state:
    st.session_state.stock_name = "RELIANCE"
if 'period' not in st.session_state:
    st.session_state.period = 60

# ----------------------- CUSTOM NAVIGATION BAR -----------------------
st.markdown(f"""
<div class="custom-navbar">
    <div class="nav-brand">PRASANTH AI TRADING INSIGHTS</div>
    
    <div class="nav-section">
        <a href="?section=Home" class="nav-button {'active' if st.session_state.current_section == 'Home' else ''}">🏠 Home</a>
        <a href="?section=Research Reports" class="nav-button {'active' if st.session_state.current_section == 'Research Reports' else ''}">📑 Research</a>
        <a href="?section=Options Trading" class="nav-button {'active' if st.session_state.current_section == 'Options Trading' else ''}">💹 Options</a>
        <a href="?section=Chart Analysis" class="nav-button {'active' if st.session_state.current_section == 'Chart Analysis' else ''}">📈 Charts</a>
        <a href="?section=AI Predictions" class="nav-button {'active' if st.session_state.current_section == 'AI Predictions' else ''}">🤖 AI Predictions</a>
    </div>
    
    <div class="stock-selector">
        <form id="stockForm">
            <select name="stock" onchange="this.form.submit()">
                <option value="RELIANCE" {'selected' if st.session_state.stock_name == 'RELIANCE' else ''}>RELIANCE</option>
                <option value="TCS" {'selected' if st.session_state.stock_name == 'TCS' else ''}>TCS</option>
                <option value="INFY" {'selected' if st.session_state.stock_name == 'INFY' else ''}>INFY</option>
                <option value="HDFC BANK" {'selected' if st.session_state.stock_name == 'HDFC BANK' else ''}>HDFC BANK</option>
                <option value="ICICI BANK" {'selected' if st.session_state.stock_name == 'ICICI BANK' else ''}>ICICI BANK</option>
                <option value="NIFTY 50" {'selected' if st.session_state.stock_name == 'NIFTY 50' else ''}>NIFTY 50</option>
                <option value="BANK NIFTY" {'selected' if st.session_state.stock_name == 'BANK NIFTY' else ''}>BANK NIFTY</option>
                <option value="AAPL" {'selected' if st.session_state.stock_name == 'AAPL' else ''}>AAPL</option>
                <option value="TSLA" {'selected' if st.session_state.stock_name == 'TSLA' else ''}>TSLA</option>
            </select>
        </form>
        
        <form id="periodForm">
            <input type="range" name="period" min="10" max="365" value="{st.session_state.period}" 
                   onchange="updatePeriodDisplay(this.value); this.form.submit()" style="width: 120px;">
        </form>
        <div class="period-display">{st.session_state.period} days</div>
    </div>
</div>

<script>
function updatePeriodDisplay(value) {{
    document.querySelector('.period-display').textContent = value + ' days';
}}
</script>
""", unsafe_allow_html=True)

# ----------------------- QUERY PARAMETERS HANDLING -----------------------
params = st.experimental_get_query_params()

# Handle section changes
if 'section' in params:
    st.session_state.current_section = params['section'][0]

# Handle stock changes
if 'stock' in params:
    st.session_state.stock_name = params['stock'][0]

# Handle period changes  
if 'period' in params:
    st.session_state.period = int(params['period'][0])

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

ticker = stocks[st.session_state.stock_name]
section = st.session_state.current_section
period = st.session_state.period

# ----------------------- HOME SECTION -----------------------
if section == "Home":
    st.markdown('<div class="main-header">PRASANTH AI TRADING INSIGHTS</div>', unsafe_allow_html=True)
    st.subheader(f"📊 {st.session_state.stock_name} - Real-Time Market Data")
    
    with st.spinner(f"Fetching {st.session_state.stock_name} data..."):
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
                st.subheader(f"{st.session_state.stock_name} Price Chart")
                
                chart_data = df[['Date', 'Close', 'SMA20', 'SMA50', 'EMA20']].copy()
                
                base = alt.Chart(chart_data).encode(x='Date:T').properties(height=400)
                
                close_line = base.mark_line(color='#00ffcc').encode(y='Close:Q', tooltip=['Date:T', 'Close:Q'])
                sma20_line = base.mark_line(color='#ffaa00', strokeDash=[5,5]).encode(y='SMA20:Q', tooltip=['Date:T', 'SMA20:Q'])
                sma50_line = base.mark_line(color='#ff00ff', strokeDash=[5,5]).encode(y='SMA50:Q', tooltip=['Date:T', 'SMA50:Q'])
                ema20_line = base.mark_line(color='#33cc33', strokeDash=[2,2]).encode(y='EMA20:Q', tooltip=['Date:T', 'EMA20:Q'])
                
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
                    x='Date:T', y='Volume:Q', tooltip=['Date:T', 'Volume:Q']
                ).properties(height=300)
                st.altair_chart(volume_chart, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")

# ----------------------- OTHER SECTIONS -----------------------
elif section == "Research Reports":
    st.markdown('<div class="main-header">RESEARCH REPORTS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="landing-box"><h2>📑 Research Reports</h2><p>Access AI-powered fundamental & technical analysis reports here.</p></div>',
        unsafe_allow_html=True,
    )
    
    try:
        df = get_stock_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**Current {st.session_state.stock_name} Price:** {current_price:.2f}")
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
    st.markdown('<div class="main-header">OPTIONS TRADING</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="landing-box"><h2>💹 Options Trading</h2><p>Monitor open interest, volatility, and strategy payoffs.</p></div>',
        unsafe_allow_html=True,
    )
    
    try:
        df = get_stock_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**Current {st.session_state.stock_name} Price:** {current_price:.2f}")
    except:
        pass
    
    st.subheader("Options Chain")
    st.info("Options data feature will be available soon.")

elif section == "Chart Analysis":
    st.markdown('<div class="main-header">CHART ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="landing-box"><h2>📈 Chart Analysis</h2><p>Advanced technical analysis with multiple indicators.</p></div>',
        unsafe_allow_html=True,
    )
    
    try:
        df = get_stock_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**Current {st.session_state.stock_name} Price:** {current_price:.2f}")
    except:
        pass
    
    st.info("Advanced chart analysis features coming soon.")

elif section == "AI Predictions":
    st.markdown('<div class="main-header">AI PREDICTIONS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="landing-box"><h2>🤖 AI Predictions</h2><p>AI-powered price predictions and trading signals.</p></div>',
        unsafe_allow_html=True,
    )
    
    try:
        df = get_stock_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**Current {st.session_state.stock_name} Price:** {current_price:.2f}")
    except:
        pass
    
    st.info("AI prediction models will be deployed soon.")

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>PRASANTH AI TRADING INSIGHTS • Real-time Market Data</div>", unsafe_allow_html=True)