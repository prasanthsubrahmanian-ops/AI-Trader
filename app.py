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

/* Hide the default sidebar collapse button */
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

.sidebar-toggle {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 9999;
    background-color: #00ffcc;
    color: #000;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0, 255, 204, 0.3);
}

.sidebar-toggle:hover {
    background-color: #00e6b8;
    transform: scale(1.1);
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

@media (max-width: 768px) {
    .landing-box { padding: 1.5rem; }
    .main-header { font-size: 2rem; text-align: center; }
    .stDataFrame { font-size: 12px; }
    .stMetric { margin: 0.2rem; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------- SIDEBAR TOGGLE BUTTON -----------------------
st.markdown("""
<script>
// Add a permanent sidebar toggle button
function addSidebarToggle() {
    const toggleBtn = document.createElement('button');
    toggleBtn.innerHTML = '☰';
    toggleBtn.className = 'sidebar-toggle';
    toggleBtn.title = 'Toggle Sidebar';
    toggleBtn.onclick = function() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            const isHidden = sidebar.style.transform === 'translateX(-100%)';
            sidebar.style.transform = isHidden ? 'translateX(0)' : 'translateX(-100%)';
        }
    };
    document.body.appendChild(toggleBtn);
}

// Run after page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addSidebarToggle);
} else {
    addSidebarToggle();
}
</script>
""", unsafe_allow_html=True)

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

# ----------------------- SESSION STATE FOR SIDEBAR -----------------------
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True

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
    st.title("📊 PRASANTH AI")
    
    # Manual sidebar toggle button inside sidebar
    if st.button("📱 Toggle Sidebar"):
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
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
    
    # Additional help text
    st.markdown("---")
    st.markdown("""
    <div style='color: #888; font-size: 0.8rem; text-align: center;'>
    💡 Use the ☰ button in the top-left to show/hide sidebar
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

# ----------------------- OTHER SECTIONS (Research Reports, Options Trading, etc.) -----------------------
# [Keep all the other sections exactly as they were in the previous code]
# Research Reports, Options Trading, Chart Analysis, AI Predictions sections remain the same...

# For brevity, I'm showing only the Home section. The other sections should be copied from the previous code.

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>PRASANTH AI TRADING INSIGHTS • Real-time Market Data</div>", unsafe_allow_html=True)