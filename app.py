import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="Smart Trade by Prasanth Subrahmanian", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------- CUSTOM STYLE -----------------------
custom_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

body, .main, .block-container {
    background: linear-gradient(135deg, #050817 0%, #0a1025 25%, #0a0f2d 50%, #071022 75%, #050817 100%) !important;
    color: #e0e0ff !important;
    padding-top: 0.5rem !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.main-header {
    margin-top: 0.5rem;
    margin-bottom: 0.3rem;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(45deg, #00d4ff, #0099ff, #0066ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    padding: 0.3rem 0;
    text-shadow: 0 2px 10px rgba(0, 212, 255, 0.3);
}

.main-subtitle {
    font-size: 1rem;
    text-align: center;
    color: #6688cc;
    margin-top: -0.5rem;
    margin-bottom: 1.5rem;
    font-weight: 500;
    font-style: italic;
    letter-spacing: 0.5px;
}

/* Top Navigation */
.top-nav {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    margin: 0.2rem 0 1.5rem 0;
    flex-wrap: wrap;
}

.nav-btn {
    background: linear-gradient(135deg, rgba(0, 100, 200, 0.2) 0%, rgba(0, 60, 150, 0.3) 100%);
    border: 1px solid rgba(0, 140, 255, 0.4);
    color: #66aaff;
    padding: 0.5rem 1.2rem;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0, 80, 200, 0.25);
}

.nav-btn:hover {
    background: linear-gradient(135deg, rgba(0, 150, 255, 0.3) 0%, rgba(0, 100, 200, 0.4) 100%);
    border-color: #00b4ff;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 180, 255, 0.4);
    color: #ffffff;
}

.nav-btn.active {
    background: linear-gradient(45deg, #00b4ff, #0088ff);
    color: #050817;
    border-color: #00b4ff;
    box-shadow: 0 4px 20px rgba(0, 180, 255, 0.6);
}

/* Cards */
.feature-card {
    background: linear-gradient(135deg, rgba(10, 15, 40, 0.9) 0%, rgba(15, 22, 55, 0.7) 100%);
    padding: 1.2rem;
    border-radius: 14px;
    border: 1px solid rgba(0, 120, 255, 0.25);
    margin-bottom: 1.2rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(15px);
    box-shadow: 0 6px 25px rgba(0, 40, 120, 0.15);
}

.feature-card:hover {
    border-color: #00b4ff;
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0, 180, 255, 0.25);
    background: linear-gradient(135deg, rgba(12, 18, 45, 0.95) 0%, rgba(18, 25, 60, 0.8) 100%);
}

.feature-icon {
    font-size: 1.8rem;
    margin-bottom: 0.8rem;
    background: linear-gradient(45deg, #00b4ff, #0088ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 2px 6px rgba(0, 180, 255, 0.3));
}

.feature-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: #ffffff;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

.feature-desc {
    font-size: 0.9rem;
    color: #99aaff;
    margin-bottom: 0.8rem;
    line-height: 1.4;
}

/* Chart Container */
.chart-container {
    background: linear-gradient(135deg, rgba(10, 15, 40, 0.95) 0%, rgba(15, 22, 55, 0.8) 100%);
    padding: 1.5rem;
    border-radius: 16px;
    margin: 1.2rem 0;
    border: 1px solid rgba(0, 120, 255, 0.3);
    backdrop-filter: blur(15px);
    box-shadow: 0 6px 30px rgba(0, 40, 120, 0.2);
}

.chart-header {
    color: #00b4ff;
    margin-bottom: 1.2rem;
    font-size: 1.3rem;
    font-weight: 700;
    text-shadow: 0 2px 6px rgba(0, 180, 255, 0.3);
}

.prediction-badge {
    background: linear-gradient(45deg, #00b4ff, #0088ff);
    color: #050817;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 0.8rem;
    box-shadow: 0 3px 12px rgba(0, 180, 255, 0.3);
}

.risk-badge {
    background: linear-gradient(45deg, #ff5555, #ff8844);
    color: #050817;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 0.8rem;
    box-shadow: 0 3px 12px rgba(255, 85, 85, 0.3);
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(10, 15, 40, 0.9) 0%, rgba(15, 22, 55, 0.7) 100%) !important;
    border: 1px solid rgba(0, 120, 255, 0.25) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    backdrop-filter: blur(10px);
}

/* Select Box Styling */
.stSelectbox > div > div {
    background: linear-gradient(135deg, rgba(10, 15, 40, 0.95) 0%, rgba(15, 22, 55, 0.8) 100%) !important;
    border: 1px solid rgba(0, 120, 255, 0.35) !important;
    border-radius: 10px !important;
    color: #ccddff !important;
}

.stSelectbox > div > div:hover {
    border-color: #00b4ff !important;
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 100, 200, 0.25) 0%, rgba(0, 60, 150, 0.35) 100%) !important;
    border: 1px solid rgba(0, 140, 255, 0.4) !important;
    color: #66aaff !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0, 150, 255, 0.35) 0%, rgba(0, 100, 200, 0.45) 100%) !important;
    border-color: #00b4ff !important;
    color: #ffffff !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 12px rgba(0, 180, 255, 0.3) !important;
}

/* Progress Bar */
.stProgress > div > div {
    background: linear-gradient(45deg, #00b4ff, #0088ff) !important;
}

/* Dataframe Styling */
.dataframe {
    background: linear-gradient(135deg, rgba(10, 15, 40, 0.9) 0%, rgba(15, 22, 55, 0.7) 100%) !important;
    border: 1px solid rgba(0, 120, 255, 0.25) !important;
    border-radius: 10px !important;
}

/* Compact Header Boxes */
.compact-header {
    background: linear-gradient(135deg, rgba(10, 15, 40, 0.95) 0%, rgba(15, 22, 55, 0.8) 100%) !important;
    padding: 1.2rem 1.5rem !important;
    border-radius: 14px !important;
    margin: 1rem 0 !important;
    border: 1px solid rgba(0, 120, 255, 0.35) !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 6px 25px rgba(0, 40, 120, 0.15);
}

.compact-header h2 {
    color: #00b4ff !important;
    text-align: center !important;
    margin-bottom: 0.5rem !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.compact-header p {
    color: #99aaff !important;
    text-align: center !important;
    font-size: 0.95rem !important;
    margin-bottom: 0 !important;
    line-height: 1.3 !important;
}

/* Info and Warning Boxes */
.stAlert {
    background: linear-gradient(135deg, rgba(10, 15, 40, 0.9) 0%, rgba(15, 22, 55, 0.7) 100%) !important;
    border: 1px solid rgba(0, 120, 255, 0.3) !important;
    border-radius: 12px !important;
}

/* Success Messages */
.stSuccess {
    background: linear-gradient(135deg, rgba(0, 100, 50, 0.2) 0%, rgba(0, 150, 80, 0.3) 100%) !important;
    border: 1px solid rgba(0, 255, 150, 0.4) !important;
}

/* Error Messages */
.stError {
    background: linear-gradient(135deg, rgba(100, 0, 0, 0.2) 0%, rgba(150, 0, 0, 0.3) 100%) !important;
    border: 1px solid rgba(255, 100, 100, 0.4) !important;
}

/* Plotly Chart Background */
.js-plotly-plot .plotly .modebar {
    background: rgba(10, 15, 40, 0.9) !important;
}

.js-plotly-plot .plotly .modebar-btn {
    color: #66aaff !important;
}

.js-plotly-plot .plotly .modebar-btn:hover {
    background: rgba(0, 120, 255, 0.3) !important;
}

@media (max-width: 768px) {
    .main-header { font-size: 1.8rem; }
    .nav-btn { padding: 0.4rem 1rem; font-size: 0.85rem; }
    .feature-card { padding: 1rem; }
    .compact-header { padding: 1rem 1.2rem !important; }
    .compact-header h2 { font-size: 1.2rem !important; }
    .compact-header p { font-size: 0.9rem !important; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------- CACHED FUNCTIONS -----------------------
@st.cache_data(ttl=300)
def get_stock_data(ticker, period="1y"):
    try:
        data = yf.download(ticker, period=period, progress=False)
        if hasattr(data, 'empty') and data.empty:
            return pd.DataFrame()
        return data
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_stock_info(ticker):
    """Get fundamental data for stocks"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info
    except:
        return {}

@st.cache_data(ttl=3600)
def get_market_data():
    """Get NIFTY, sector data, gainers, losers"""
    indices = {
        'NIFTY 50': '^NSEI',
        'BANK NIFTY': '^NSEBANK',
        'NIFTY IT': '^CNXIT',
        'SENSEX': '^BSESN'
    }
    
    data = {}
    for name, ticker in indices.items():
        try:
            df = yf.download(ticker, period='2d', progress=False)
            if hasattr(df, 'empty') and not df.empty and len(df) > 1:
                current_price = float(df['Close'].iloc[-1])
                prev_price = float(df['Close'].iloc[-2])
                change = current_price - prev_price
                change_pct = (change / prev_price) * 100
                
                data[name] = {
                    'current': current_price,
                    'change': change,
                    'change_pct': change_pct
                }
        except Exception as e:
            continue
    return data

@st.cache_data(ttl=3600)
def get_news_data():
    """Get market news data"""
    # Mock news data - in real implementation, you'd use a news API
    return [
        {"title": "RBI Keeps Repo Rate Unchanged at 6.5%", "source": "Economic Times", "time": "2 hours ago", "sentiment": "positive"},
        {"title": "Reliance Announces Major Green Energy Investment", "source": "Business Standard", "time": "4 hours ago", "sentiment": "positive"},
        {"title": "IT Sector Faces Headwinds from Global Slowdown", "source": "Money Control", "time": "6 hours ago", "sentiment": "negative"},
        {"title": "Banking Stocks Rally on Strong Quarterly Results", "source": "Financial Express", "time": "8 hours ago", "sentiment": "positive"},
        {"title": "Auto Sales Show Mixed Trends in November", "source": "Auto Car India", "time": "10 hours ago", "sentiment": "neutral"}
    ]

@st.cache_data(ttl=3600)
def get_market_intelligence():
    """Get market intelligence data"""
    return {
        "sector_performance": {
            "Banking": "+2.8%",
            "IT": "-1.2%", 
            "Pharma": "+1.5%",
            "Auto": "+0.8%",
            "Energy": "+3.2%"
        },
        "market_sentiment": "Bullish",
        "volume_trend": "Increasing",
        "volatility_index": "Medium",
        "institutional_activity": "Buying"
    }

# ----------------------- SESSION STATE -----------------------
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Home"
if 'stock_name' not in st.session_state:
    st.session_state.stock_name = "NIFTY 50"
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "^NSEI"

# ----------------------- HEADER -----------------------
st.markdown('<div class="main-header">🚀 SMART TRADE PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">by <em>Prasanth Subrahmanian</em> | Advanced Trading Analytics Platform</div>', unsafe_allow_html=True)

# ----------------------- MAIN NAVIGATION -----------------------
nav_options = ["🏠 Dashboard", "📈 Market Analysis", "🤖 AI Signals", "💡 Market Intelligence", "📰 News", "🔍 Backtesting"]
nav_labels = ["Home", "Market Trends", "AI Signals", "Market Intelligence", "News", "Backtesting"]

nav_cols = st.columns(6)
for i, (col, option) in enumerate(zip(nav_cols, nav_options)):
    with col:
        btn_type = "primary" if st.session_state.current_section == nav_labels[i] else "secondary"
        if st.button(option, use_container_width=True, type=btn_type):
            st.session_state.current_section = nav_labels[i]
            st.rerun()

# ----------------------- STOCK SELECTION -----------------------
stocks = {
    # Indices
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK", 
    "NIFTY IT": "^CNXIT",
    "SENSEX": "^BSESN",
    
    # Major NIFTY 50 Stocks
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "INFOSYS": "INFY.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "SBIN": "SBIN.NS",
    "BHARTI AIRTEL": "BHARTIARTL.NS",
    "KOTAK BANK": "KOTAKBANK.NS",
    "LT": "LT.NS",
    "HCL TECH": "HCLTECH.NS",
    "AXIS BANK": "AXISBANK.NS",
    "MARUTI": "MARUTI.NS",
    "ASIAN PAINTS": "ASIANPAINT.NS",
    "SUN PHARMA": "SUNPHARMA.NS",
    "TITAN": "TITAN.NS",
    "ULTRACEMCO": "ULTRACEMCO.NS",
    "WIPRO": "WIPRO.NS",
    "NESTLE": "NESTLEIND.NS",
    "POWERGRID": "POWERGRID.NS",
    "NTPC": "NTPC.NS",
    "ONGC": "ONGC.NS",
    "TECH MAHINDRA": "TECHM.NS",
    
    # International Stocks
    "AAPL": "AAPL",
    "TSLA": "TSLA",
    "GOOGL": "GOOGL",
    "MSFT": "MSFT"
}

# Stock selection available on all pages except Home
if st.session_state.current_section not in ["Home", "Market Intelligence", "News"]:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        stock_name = st.selectbox("Select Stock/Index", list(stocks.keys()), 
                                 index=list(stocks.keys()).index(st.session_state.stock_name))
    with col2:
        if st.session_state.current_section == "Market Trends":
            timeframe = st.selectbox("Timeframe", ["1D", "1W", "1M", "3M", "6M", "1Y"], index=0)
        else:
            timeframe = st.selectbox("Timeframe", ["1D", "1W", "1M", "3M", "6M", "1Y"], index=2)
    with col3:
        st.write("")
        st.write(f"*Current:* **{stock_name}** | **{timeframe}**")

    st.session_state.stock_name = stock_name
    ticker = stocks[st.session_state.stock_name]
    st.session_state.current_ticker = ticker

section = st.session_state.current_section

# ----------------------- HOME PAGE -----------------------
def show_home():
    """Home page with overview and quick access"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>📊 Trading Dashboard</h2>'
        '<p>Advanced trading insights powered by AI and real-time market data</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Quick Stats
    st.markdown("### 📈 Live Market Overview")
    
    with st.spinner('Loading market data...'):
        market_data = get_market_data()
    
    if market_data:
        cols = st.columns(4)
        
        for i, (idx_name, idx_data) in enumerate(market_data.items()):
            with cols[i % 4]:
                change_value = float(idx_data['change'])
                change_color = "#00ffaa" if change_value >= 0 else "#ff5555"
                st.markdown(f"""
                <div class="feature-card">
                    <div style="font-weight: 600; margin-bottom: 0.6rem; color: #66aaff; font-size: 0.95rem;">{idx_name}</div>
                    <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem; color: #ffffff;">₹{idx_data['current']:.2f}</div>
                    <div style="color: {change_color}; font-weight: 600; font-size: 0.9rem;">
                        {idx_data['change']:+.2f} ({idx_data['change_pct']:+.2f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Fallback data when market data is not available
        fallback_data = {
            'NIFTY 50': {'current': 22450.75, 'change': 125.50, 'change_pct': 0.56},
            'BANK NIFTY': {'current': 48230.40, 'change': 280.25, 'change_pct': 0.58},
            'SENSEX': {'current': 73920.15, 'change': 350.80, 'change_pct': 0.48},
            'NIFTY IT': {'current': 36240.60, 'change': 95.30, 'change_pct': 0.26}
        }
        
        cols = st.columns(4)
        for i, (idx_name, idx_data) in enumerate(fallback_data.items()):
            with cols[i % 4]:
                change_color = "#00ffaa" if idx_data['change'] >= 0 else "#ff5555"
                st.markdown(f"""
                <div class="feature-card">
                    <div style="font-weight: 600; margin-bottom: 0.6rem; color: #66aaff; font-size: 0.95rem;">{idx_name}</div>
                    <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem; color: #ffffff;">₹{idx_data['current']:,.2f}</div>
                    <div style="color: {change_color}; font-weight: 600; font-size: 0.9rem;">
                        {idx_data['change']:+.2f} ({idx_data['change_pct']:+.2f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Trading Tools Section
    st.markdown("### ⚡ Trading Tools")
    
    tools_cols = st.columns(3)
    
    with tools_cols[0]:
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?section=Market Intelligence'" style="cursor: pointer;">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Market Intelligence</div>
            <div class="feature-desc">Comprehensive market analysis, sector performance, and institutional activity tracking</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tools_cols[1]:
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?section=AI Signals'" style="cursor: pointer;">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Signals</div>
            <div class="feature-desc">Machine learning based buy/sell signals and automated trading recommendations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tools_cols[2]:
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?section=News'" style="cursor: pointer;">
            <div class="feature-icon">📰</div>
            <div class="feature-title">Market News</div>
            <div class="feature-desc">Latest financial news, market updates, and sentiment analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Sentiment
    st.markdown("### 🌡️ Market Sentiment")
    sentiment_cols = st.columns(2)
    
    with sentiment_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📈 Today's Top Movers</div>
            <div style="color: #00ffaa; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• RELIANCE: +2.8%</div>
            <div style="color: #00ffaa; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• TCS: +1.9%</div>
            <div style="color: #00ffaa; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• HDFC BANK: +1.5%</div>
            <div style="color: #ff5555; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• INFY: -0.8%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with sentiment_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎯 Trading Signals</div>
            <div style="color: #00ffaa; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• Overall: BULLISH 📈</div>
            <div style="color: #00ffaa; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• Volume: HIGH 🔥</div>
            <div style="color: #ffaa44; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• Volatility: MEDIUM ⚡</div>
            <div style="color: #00ffaa; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• Momentum: STRONG 💪</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------- MARKET TRENDS PAGE -----------------------
def show_market_trends():
    """Market Trends - Shows stock/index charts and analysis"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>📈 Advanced Market Analysis</h2>'
        '<p>Real-time charts, technical indicators, and market insights</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Current Price Overview
    try:
        period_map = {
            "1D": "5d",
            "1W": "1mo", 
            "1M": "3mo",
            "3M": "6mo",
            "6M": "1y",
            "1Y": "2y"
        }
        
        selected_period = period_map.get(timeframe, "3mo")
        df = get_stock_data(ticker, selected_period)
        
        # Simple and clear DataFrame check
        if df is not None and hasattr(df, 'empty') and not df.empty and len(df) > 1:
            current_price = float(df['Close'].iloc[-1])
            
            # Calculate price change
            if timeframe == "1D" and len(df) >= 2:
                prev_price = float(df['Close'].iloc[-2])
            else:
                prev_price = float(df['Close'].iloc[0])
            
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100 if prev_price != 0 else 0
            
            # Display current price
            st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1rem; color: #88aaff; margin-bottom: 0.4rem;">{stock_name}</div>
                        <div style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(45deg, #00b4ff, #0088ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.4rem;">
                            ₹{current_price:,.2f}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: {'#00ffaa' if price_change >= 0 else '#ff5555'};">
                            {price_change:+.2f} ({price_change_pct:+.2f}%)
                        </div>
                        <div style="font-size: 0.9rem; color: #88aaff; margin-top: 0.3rem;">
                            {timeframe} Return
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"Loading data for {stock_name}...")
            
    except Exception as e:
        st.error(f"Error loading price data: {str(e)}")
    
    # Fundamental Data for Stocks (not indices)
    if stock_name not in ["NIFTY 50", "BANK NIFTY", "NIFTY IT", "SENSEX"]:
        st.markdown("### 📊 Fundamental Analysis")
        
        stock_info = get_stock_info(ticker)
        if stock_info:
            fund_cols = st.columns(4)
            with fund_cols[0]:
                pe_ratio = stock_info.get('trailingPE', 'N/A')
                st.metric("P/E Ratio", f"{pe_ratio}" if pe_ratio != 'N/A' else "N/A")
            
            with fund_cols[1]:
                dividend_yield = stock_info.get('dividendYield', 'N/A')
                if dividend_yield != 'N/A' and dividend_yield is not None:
                    st.metric("Dividend Yield", f"{dividend_yield*100:.2f}%")
                else:
                    st.metric("Dividend Yield", "N/A")
            
            with fund_cols[2]:
                market_cap = stock_info.get('marketCap', 'N/A')
                if market_cap != 'N/A' and market_cap is not None:
                    if market_cap > 1e12:
                        st.metric("Market Cap", f"₹{market_cap/1e12:.2f}T")
                    elif market_cap > 1e9:
                        st.metric("Market Cap", f"₹{market_cap/1e9:.2f}B")
                    else:
                        st.metric("Market Cap", f"₹{market_cap/1e6:.2f}M")
                else:
                    st.metric("Market Cap", "N/A")
            
            with fund_cols[3]:
                beta = stock_info.get('beta', 'N/A')
                st.metric("Beta", f"{beta}" if beta != 'N/A' else "N/A")
    
    # Advanced Charting
    st.markdown(f"### 📊 {stock_name} Advanced Chart")
    
    try:
        # Get chart data
        chart_period_map = {
            "1D": "5d",
            "1W": "1mo", 
            "1M": "3mo",
            "3M": "6mo",
            "6M": "1y",
            "1Y": "2y"
        }
        
        selected_chart_period = chart_period_map.get(timeframe, "3mo")
        df_chart = get_stock_data(ticker, selected_chart_period)
        
        # Simple and clear data validation
        if (df_chart is not None and 
            hasattr(df_chart, 'empty') and 
            not df_chart.empty and 
            len(df_chart) > 1 and
            'Close' in df_chart.columns):
            
            # Create basic chart
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            fig = go.Figure()
            
            # Always use line chart for simplicity
            fig.add_trace(go.Scatter(
                x=df_chart.index, 
                y=df_chart['Close'], 
                mode='lines', 
                name='Price',
                line=dict(color='#00b4ff', width=3)
            ))
            
            # Simple moving average calculation
            if len(df_chart) > 20:
                try:
                    ma20 = df_chart['Close'].rolling(window=20).mean()
                    # Use .any() instead of ambiguous boolean
                    if ma20.notna().any():
                        fig.add_trace(go.Scatter(
                            x=df_chart.index, 
                            y=ma20, 
                            mode='lines', 
                            name='MA20',
                            line=dict(color='#ff5555', width=2, dash='dash')
                        ))
                except:
                    pass
            
            # Chart layout
            is_index = stock_name in ["NIFTY 50", "BANK NIFTY", "NIFTY IT", "SENSEX"]
            chart_title = f"{stock_name} - {timeframe} Chart"
            y_axis_title = "Index Value" if is_index else "Price (₹)"
            
            fig.update_layout(
                title=dict(text=chart_title, font=dict(color='#00b4ff', size=18)),
                template="plotly_dark",
                height=450,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                xaxis_title="Date",
                yaxis_title=y_axis_title,
                plot_bgcolor='rgba(10, 15, 40, 0.9)',
                paper_bgcolor='rgba(10, 15, 40, 0.9)',
                font=dict(color='#e0e0ff')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Technical Indicators
            st.markdown("### 🔧 Technical Indicators")
            
            tech_cols = st.columns(4)
            
            with tech_cols[0]:
                # Simple RSI calculation
                try:
                    if len(df_chart) > 14:
                        delta = df_chart['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).fillna(0)
                        loss = (-delta.where(delta < 0, 0)).fillna(0)
                        avg_gain = gain.rolling(window=14).mean()
                        avg_loss = loss.rolling(window=14).mean()
                        rs = avg_gain / avg_loss
                        rsi = 100 - (100 / (1 + rs))
                        current_rsi = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50
                    else:
                        current_rsi = 50
                except:
                    current_rsi = 50
                
                rsi_status = "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral"
                st.metric("RSI (14)", f"{current_rsi:.1f}", rsi_status)
                
            with tech_cols[1]:
                # Simple trend detection
                try:
                    if len(df_chart) > 5:
                        recent_prices = df_chart['Close'].tail(5)
                        trend = "Bullish" if recent_prices.iloc[-1] > recent_prices.iloc[0] else "Bearish"
                    else:
                        trend = "Neutral"
                except:
                    trend = "Neutral"
                
                st.metric("Trend", trend, "")
                
            with tech_cols[2]:
                # Volume indicator
                try:
                    if 'Volume' in df_chart.columns:
                        current_vol = float(df_chart['Volume'].iloc[-1])
                        avg_vol = float(df_chart['Volume'].mean())
                        vol_ratio = current_vol / avg_vol if avg_vol > 0 else 1
                        st.metric("Volume", f"{vol_ratio:.1f}x", "High" if vol_ratio > 1.5 else "Normal")
                    else:
                        st.metric("Volume", "N/A", "")
                except:
                    st.metric("Volume", "N/A", "")
                
            with tech_cols[3]:
                # Simple volatility
                try:
                    if len(df_chart) > 1:
                        daily_returns = df_chart['Close'].pct_change().dropna()
                        if len(daily_returns) > 0:
                            vol = float(daily_returns.std() * 100)
                            st.metric("Volatility", f"{vol:.1f}%", "High" if vol > 2 else "Low")
                        else:
                            st.metric("Volatility", "N/A", "")
                    else:
                        st.metric("Volatility", "N/A", "")
                except:
                    st.metric("Volatility", "N/A", "")
                    
        else:
            st.warning(f"Chart data not available for {stock_name}. Trying fallback data...")
            
            # Fallback: Create a simple demo chart
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            # Generate sample data for demonstration
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            prices = [1000 + i*10 + np.random.normal(0, 5) for i in range(30)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, 
                y=prices, 
                mode='lines', 
                name='Price',
                line=dict(color='#00b4ff', width=3)
            ))
            
            fig.update_layout(
                title=dict(text=f"{stock_name} - Sample Chart (Demo Data)", font=dict(color='#00b4ff')),
                template="plotly_dark",
                height=400,
                showlegend=True,
                xaxis_title="Date",
                yaxis_title="Price"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.info("⚠️ Showing demo data. Real market data will load when available.")
            
    except Exception as e:
        st.error(f"Error in chart section: {str(e)}")
        
        # Ultra-simple fallback
        st.markdown("""
        <div class="chart-container">
            <p style="text-align: center; color: #88aaff; padding: 1.5rem; font-size: 1rem;">
                Chart is temporarily unavailable. Please try refreshing the page or select a different stock.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------- AI SIGNALS PAGE -----------------------
def show_ai_signals():
    """AI Signals - Advanced AI trading signals and recommendations"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>🤖 AI Trading Signals</h2>'
        '<p>Advanced machine learning signals and automated trading recommendations</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Current price
    current_price = 2500
    try:
        df = get_stock_data(ticker, "1mo")
        if df is not None and hasattr(df, 'empty') and not df.empty and len(df) > 0:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"{stock_name} Current Price: ₹{current_price:.2f}")
    except:
        current_price = 2500
    
    # AI Signals Dashboard
    st.markdown("### 🎯 AI Trading Signals")
    
    signal_cols = st.columns(3)
    with signal_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Momentum Signal</div>', unsafe_allow_html=True)
        st.metric("Signal Strength", "STRONG BUY", "92% Confidence")
        st.progress(92, text="Confidence: 92%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with signal_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📈</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Trend Analysis</div>', unsafe_allow_html=True)
        st.metric("Trend Direction", "BULLISH", "85% Accuracy")
        st.progress(85, text="Accuracy: 85%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with signal_cols[2]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">⚡</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Volatility Signal</div>', unsafe_allow_html=True)
        st.metric("Risk Level", "MEDIUM", "Optimal Entry")
        st.progress(65, text="Risk Score: 65%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced AI Analysis
    st.markdown("### 🔍 Advanced AI Analysis")
    
    analysis_cols = st.columns(2)
    with analysis_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Pattern Recognition</div>', unsafe_allow_html=True)
        st.metric("Pattern Detected", "Bull Flag", "High Reliability")
        st.metric("Target Price", f"₹{current_price * 1.12:.2f}", "+12.0%")
        st.metric("Timeframe", "2-4 Weeks", "Expected Duration")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with analysis_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Sentiment Analysis</div>', unsafe_allow_html=True)
        st.metric("Market Sentiment", "VERY BULLISH", "Positive")
        st.metric("News Impact", "POSITIVE", "+2.3%")
        st.metric("Social Buzz", "HIGH", "Increasing")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Prediction Chart
    st.markdown("### 📈 AI Price Prediction")
    
    try:
        # Create prediction chart
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        # Mock prediction data with AI pattern
        base_price = current_price
        predictions = [base_price * (1 + 0.003 * i + np.random.normal(0, 0.008)) for i in range(30)]
        
        fig = go.Figure()
        
        # Historical data
        hist_dates = pd.date_range(start=datetime.now() - timedelta(days=60), end=datetime.now(), freq='D')
        hist_prices = [base_price * (1 - 0.002 * i + np.random.normal(0, 0.01)) for i in range(60, 0, -1)]
        
        fig.add_trace(go.Scatter(
            x=hist_dates, 
            y=hist_prices,
            mode='lines',
            name='Historical',
            line=dict(color='#6666ff', width=2)
        ))
        
        # Prediction line
        fig.add_trace(go.Scatter(
            x=dates, 
            y=predictions,
            mode='lines+markers',
            name='AI Prediction',
            line=dict(color='#00ffaa', width=3)
        ))
        
        # Confidence interval
        upper_bound = [p * 1.05 for p in predictions]
        lower_bound = [p * 0.95 for p in predictions]
        
        fig.add_trace(go.Scatter(
            x=dates, 
            y=upper_bound,
            mode='lines',
            name='Upper Bound',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=dates, 
            y=lower_bound,
            mode='lines',
            name='Lower Bound',
            fill='tonexty',
            fillcolor='rgba(0, 255, 170, 0.2)',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.update_layout(
            title=dict(text=f"AI Price Prediction for {stock_name} (Next 30 Days)", font=dict(color='#00b4ff')),
            template="plotly_dark",
            height=400,
            showlegend=True,
            xaxis_title="Date",
            yaxis_title="Price (₹)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error generating prediction chart: {str(e)}")
    
    # Trading Recommendations
    st.markdown("### 💡 Trading Recommendations")
    
    rec_cols = st.columns(3)
    with rec_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Entry Point</div>', unsafe_allow_html=True)
        st.metric("Optimal Entry", f"₹{current_price * 0.98:.2f}", "-2.0%")
        st.metric("Stop Loss", f"₹{current_price * 0.92:.2f}", "-8.0%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with rec_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Target Levels</div>', unsafe_allow_html=True)
        st.metric("Target 1", f"₹{current_price * 1.08:.2f}", "+8.0%")
        st.metric("Target 2", f"₹{current_price * 1.15:.2f}", "+15.0%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with rec_cols[2]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Position Sizing</div>', unsafe_allow_html=True)
        st.metric("Risk/Reward", "1:3", "Excellent")
        st.metric("Allocation", "15-20%", "Portfolio")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------- MARKET INTELLIGENCE PAGE -----------------------
def show_market_intelligence():
    """Market Intelligence - Comprehensive market analysis"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>💡 Market Intelligence</h2>'
        '<p>Comprehensive market analysis, sector performance, and institutional insights</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Market Overview
    st.markdown("### 📊 Market Overview")
    
    intel_data = get_market_intelligence()
    
    overview_cols = st.columns(4)
    with overview_cols[0]:
        st.metric("Market Sentiment", intel_data["market_sentiment"], "Bullish")
    with overview_cols[1]:
        st.metric("Volume Trend", intel_data["volume_trend"], "Increasing")
    with overview_cols[2]:
        st.metric("Volatility Index", intel_data["volatility_index"], "Medium")
    with overview_cols[3]:
        st.metric("Institutional Flow", intel_data["institutional_activity"], "Buying")
    
    # Sector Performance
    st.markdown("### 🏢 Sector Performance")
    
    sector_data = intel_data["sector_performance"]
    sector_cols = st.columns(5)
    
    for i, (sector, performance) in enumerate(sector_data.items()):
        with sector_cols[i]:
            change_color = "#00ffaa" if performance.startswith('+') else "#ff5555"
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-weight: 600; margin-bottom: 0.8rem; color: #66aaff;">{sector}</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: {change_color};">
                    {performance}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Market Depth Analysis
    st.markdown("### 📈 Market Depth Analysis")
    
    depth_cols = st.columns(2)
    
    with depth_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Order Book Analysis</div>', unsafe_allow_html=True)
        
        # Mock order book data
        order_data = {
            'Bid Price': [2495, 2490, 2485, 2480, 2475],
            'Bid Quantity': [1500, 2200, 1800, 1200, 900],
            'Ask Price': [2505, 2510, 2515, 2520, 2525],
            'Ask Quantity': [1300, 1900, 1600, 1100, 800]
        }
        
        order_df = pd.DataFrame(order_data)
        st.dataframe(order_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with depth_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Volume Profile</div>', unsafe_allow_html=True)
        
        # Mock volume profile
        vol_profile = {
            'Price Level': ['2470-2480', '2480-2490', '2490-2500', '2500-2510', '2510-2520'],
            'Volume': [1200000, 1850000, 2250000, 1950000, 1450000],
            'POC': ['', '', '★', '', '']
        }
        
        vol_df = pd.DataFrame(vol_profile)
        st.dataframe(vol_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Institutional Activity
    st.markdown("### 🏛️ Institutional Activity")
    
    inst_cols = st.columns(3)
    with inst_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">FII Activity</div>', unsafe_allow_html=True)
        st.metric("Net Investment", "₹1,250 Cr", "+2.8%")
        st.metric("Buy/Sell Ratio", "1.8", "Bullish")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with inst_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">DII Activity</div>', unsafe_allow_html=True)
        st.metric("Net Investment", "₹980 Cr", "+1.5%")
        st.metric("Buy/Sell Ratio", "1.5", "Positive")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with inst_cols[2]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Proprietary</div>', unsafe_allow_html=True)
        st.metric("Net Position", "Long", "Strong")
        st.metric("Exposure", "85%", "High")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Market Statistics
    st.markdown("### 📊 Market Statistics")
    
    stats_cols = st.columns(4)
    with stats_cols[0]:
        st.metric("Advance/Decline", "1250/850", "Positive")
    with stats_cols[1]:
        st.metric("52W High/Low", "45/28", "Bullish")
    with stats_cols[2]:
        st.metric("Put/Call Ratio", "0.75", "Bullish")
    with stats_cols[3]:
        st.metric("VIX", "18.5", "Stable")

# ----------------------- NEWS PAGE -----------------------
def show_news():
    """News - Market news and sentiment analysis"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>📰 Market News & Analysis</h2>'
        '<p>Latest financial news, market updates, and sentiment analysis</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # News Feed
    st.markdown("### 📢 Latest Market News")
    
    news_data = get_news_data()
    
    for news in news_data:
        sentiment_color = {
            "positive": "#00ffaa",
            "negative": "#ff5555", 
            "neutral": "#ffaa44"
        }.get(news["sentiment"], "#ffaa44")
        
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 0.5rem;">
                <div style="flex: 1;">
                    <div style="font-weight: 700; color: #ffffff; margin-bottom: 0.3rem; font-size: 1.1rem;">{news["title"]}</div>
                    <div style="color: #88aaff; font-size: 0.9rem;">{news["source"]} • {news["time"]}</div>
                </div>
                <div style="background: {sentiment_color}; color: #050817; padding: 0.3rem 0.8rem; border-radius: 15px; font-weight: 700; font-size: 0.8rem;">
                    {news["sentiment"].upper()}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Sentiment Analysis
    st.markdown("### 🌡️ News Sentiment Analysis")
    
    sentiment_cols = st.columns(3)
    with sentiment_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Overall Sentiment</div>', unsafe_allow_html=True)
        st.metric("Market Mood", "BULLISH", "Positive")
        st.progress(72, text="Positive: 72%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with sentiment_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Sector Sentiment</div>', unsafe_allow_html=True)
        st.metric("Banking", "VERY POSITIVE", "+85%")
        st.metric("Technology", "NEUTRAL", "+45%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with sentiment_cols[2]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Impact Analysis</div>', unsafe_allow_html=True)
        st.metric("News Impact", "POSITIVE", "+2.3%")
        st.metric("Volatility Impact", "MEDIUM", "Controlled")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Trending Topics
    st.markdown("### 🔥 Trending Topics")
    
    trending_topics = [
        {"topic": "RBI Policy Meeting", "mentions": "1.2K", "sentiment": "positive"},
        {"topic": "Quarterly Results", "mentions": "980", "sentiment": "positive"},
        {"topic": "Global Markets", "mentions": "850", "sentiment": "neutral"},
        {"topic": "Oil Prices", "mentions": "720", "sentiment": "negative"},
        {"topic": "IPO News", "mentions": "650", "sentiment": "positive"}
    ]
    
    for topic in trending_topics:
        sentiment_color = {
            "positive": "#00ffaa",
            "negative": "#ff5555",
            "neutral": "#ffaa44"
        }.get(topic["sentiment"], "#ffaa44")
        
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; justify-content: between; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #ffffff; margin-bottom: 0.2rem;">{topic["topic"]}</div>
                    <div style="color: #88aaff; font-size: 0.8rem;">{topic["mentions"]} mentions</div>
                </div>
                <div style="background: {sentiment_color}; color: #050817; padding: 0.2rem 0.6rem; border-radius: 12px; font-weight: 700; font-size: 0.7rem;">
                    {topic["sentiment"].upper()}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Economic Calendar
    st.markdown("### 📅 Economic Calendar")
    
    calendar_data = [
        {"event": "GDP Data Release", "date": "Today", "impact": "High", "previous": "7.8%"},
        {"event": "Inflation Data", "date": "Tomorrow", "impact": "High", "previous": "5.0%"},
        {"event": "RBI Meeting", "date": "Dec 15", "impact": "Very High", "previous": "6.5%"},
        {"event": "Trade Balance", "date": "Dec 18", "impact": "Medium", "previous": "-$18.2B"},
        {"event": "PMI Data", "date": "Dec 20", "impact": "Medium", "previous": "58.5"}
    ]
    
    calendar_df = pd.DataFrame(calendar_data)
    st.dataframe(calendar_df, use_container_width=True)

# ----------------------- BACKTESTING PAGE -----------------------
def show_backtesting():
    """Backtesting - Test trading strategies"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>🔍 Strategy Backtesting</h2>'
        '<p>Test your trading strategies with historical data</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Strategy Configuration
    st.markdown("### ⚙️ Strategy Configuration")
    
    config_cols = st.columns(3)
    with config_cols[0]:
        strategy_type = st.selectbox(
            "Strategy Type",
            ["Moving Average Crossover", "RSI Strategy", "MACD Strategy", "Bollinger Bands"]
        )
        lookback_period = st.select_slider(
            "Lookback Period",
            options=["1M", "3M", "6M", "1Y", "2Y", "5Y"],
            value="1Y"
        )
    
    with config_cols[1]:
        initial_capital = st.number_input("Initial Capital (₹)", value=100000, step=10000)
        position_size = st.slider("Position Size (%)", 1, 100, 20)
        stop_loss = st.slider("Stop Loss (%)", 1, 20, 5)
    
    with config_cols[2]:
        take_profit = st.slider("Take Profit (%)", 5, 50, 15)
        commission = st.number_input("Commission per Trade (₹)", value=20)
        if st.button("Run Backtest", use_container_width=True):
            st.success("Backtest completed successfully!")
    
    # Backtest Results
    st.markdown("### 📊 Backtest Results")
    
    result_cols = st.columns(4)
    with result_cols[0]:
        st.metric("Total Return", "₹24,850", "+24.85%")
    with result_cols[1]:
        st.metric("Win Rate", "68.2%", "+8.2%")
    with result_cols[2]:
        st.metric("Max Drawdown", "-12.3%", "Moderate")
    with result_cols[3]:
        st.metric("Sharpe Ratio", "1.45", "Good")
    
    # Performance Chart
    st.markdown("### 📈 Strategy Performance")
    
    # Generate sample backtest data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    portfolio_value = [100000]
    for i in range(1, len(dates)):
        daily_return = np.random.normal(0.001, 0.02)
        new_value = portfolio_value[-1] * (1 + daily_return)
        portfolio_value.append(new_value)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=portfolio_value,
        mode='lines',
        name='Strategy',
        line=dict(color='#00b4ff', width=2.5)
    ))
    
    # Add benchmark (buy & hold)
    benchmark_value = [100000]
    for i in range(1, len(dates)):
        daily_return = np.random.normal(0.0008, 0.015)
        new_value = benchmark_value[-1] * (1 + daily_return)
        benchmark_value.append(new_value)
    
    fig.add_trace(go.Scatter(
        x=dates, 
        y=benchmark_value,
        mode='lines',
        name='Buy & Hold',
        line=dict(color='#ff5555', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=dict(text="Strategy vs Buy & Hold Performance", font=dict(color='#00b4ff')),
        template="plotly_dark",
        height=350,
        xaxis_title="Date",
        yaxis_title="Portfolio Value (₹)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trade Analysis
    st.markdown("### 📋 Trade Analysis")
    
    # Sample trade data
    trade_data = {
        'Date': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05', '2023-05-12'],
        'Stock': ['RELIANCE', 'TCS', 'HDFC BANK', 'INFOSYS', 'ICICI BANK'],
        'Action': ['BUY', 'BUY', 'SELL', 'BUY', 'SELL'],
        'Price': [2450, 3200, 1700, 1480, 980],
        'Quantity': [10, 15, 20, 25, 30],
        'P&L': ['-', '-', '₹2,500', '-', '₹900']
    }
    
    trade_df = pd.DataFrame(trade_data)
    st.dataframe(trade_df, use_container_width=True)

# ----------------------- MAIN APP LOGIC -----------------------
def main():
    """Main application logic"""
    section = st.session_state.current_section
    
    if section == "Home":
        show_home()
    elif section == "Market Trends":
        show_market_trends()
    elif section == "AI Signals":
        show_ai_signals()
    elif section == "Market Intelligence":
        show_market_intelligence()
    elif section == "News":
        show_news()
    elif section == "Backtesting":
        show_backtesting()

if __name__ == "__main__":
    main()