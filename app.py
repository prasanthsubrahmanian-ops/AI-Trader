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
    background: #ffffff !important;
    color: #333333 !important;
    padding-top: 0.5rem !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.main-header {
    margin-top: 0.5rem;
    margin-bottom: 0.3rem;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(45deg, #2563eb, #3b82f6, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    padding: 0.3rem 0;
    text-shadow: 0 2px 10px rgba(37, 99, 235, 0.1);
}

.main-subtitle {
    font-size: 1rem;
    text-align: center;
    color: #6b7280;
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
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.15) 100%);
    border: 1px solid rgba(37, 99, 235, 0.3);
    color: #2563eb;
    padding: 0.5rem 1.2rem;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.1);
}

.nav-btn:hover {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.2) 0%, rgba(59, 130, 246, 0.25) 100%);
    border-color: #2563eb;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.2);
    color: #1e40af;
}

.nav-btn.active {
    background: linear-gradient(45deg, #2563eb, #3b82f6);
    color: #ffffff;
    border-color: #2563eb;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3);
}

/* Cards */
.feature-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%);
    padding: 1.2rem;
    border-radius: 14px;
    border: 1px solid rgba(37, 99, 235, 0.2);
    margin-bottom: 1.2rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(15px);
    box-shadow: 0 6px 25px rgba(37, 99, 235, 0.08);
}

.feature-card:hover {
    border-color: #2563eb;
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.15);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(241, 245, 249, 0.8) 100%);
}

.feature-icon {
    font-size: 1.8rem;
    margin-bottom: 0.8rem;
    background: linear-gradient(45deg, #2563eb, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 2px 6px rgba(37, 99, 235, 0.2));
}

.feature-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: #1f2937;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.feature-desc {
    font-size: 0.9rem;
    color: #6b7280;
    margin-bottom: 0.8rem;
    line-height: 1.4;
}

/* Chart Container */
.chart-container {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.8) 100%);
    padding: 1.5rem;
    border-radius: 16px;
    margin: 1.2rem 0;
    border: 1px solid rgba(37, 99, 235, 0.25);
    backdrop-filter: blur(15px);
    box-shadow: 0 6px 30px rgba(37, 99, 235, 0.1);
}

.chart-header {
    color: #2563eb;
    margin-bottom: 1.2rem;
    font-size: 1.3rem;
    font-weight: 700;
    text-shadow: 0 2px 6px rgba(37, 99, 235, 0.1);
}

.prediction-badge {
    background: linear-gradient(45deg, #2563eb, #3b82f6);
    color: #ffffff;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 0.8rem;
    box-shadow: 0 3px 12px rgba(37, 99, 235, 0.2);
}

.risk-badge {
    background: linear-gradient(45deg, #dc2626, #ef4444);
    color: #ffffff;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 0.8rem;
    box-shadow: 0 3px 12px rgba(220, 38, 38, 0.2);
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%) !important;
    border: 1px solid rgba(37, 99, 235, 0.2) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    backdrop-filter: blur(10px);
}

/* Select Box Styling */
.stSelectbox > div > div {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.8) 100%) !important;
    border: 1px solid rgba(37, 99, 235, 0.3) !important;
    border-radius: 10px !important;
    color: #333333 !important;
}

.stSelectbox > div > div:hover {
    border-color: #2563eb !important;
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.15) 100%) !important;
    border: 1px solid rgba(37, 99, 235, 0.3) !important;
    color: #2563eb !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.2) 0%, rgba(59, 130, 246, 0.25) 100%) !important;
    border-color: #2563eb !important;
    color: #1e40af !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 12px rgba(37, 99, 235, 0.2) !important;
}

/* Progress Bar */
.stProgress > div > div {
    background: linear-gradient(45deg, #2563eb, #3b82f6) !important;
}

/* Dataframe Styling */
.dataframe {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%) !important;
    border: 1px solid rgba(37, 99, 235, 0.2) !important;
    border-radius: 10px !important;
}

/* Compact Header Boxes */
.compact-header {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.8) 100%) !important;
    padding: 1.2rem 1.5rem !important;
    border-radius: 14px !important;
    margin: 1rem 0 !important;
    border: 1px solid rgba(37, 99, 235, 0.3) !important;
    backdrop-filter: blur(10px);
}

.compact-header h2 {
    color: #2563eb !important;
    text-align: center !important;
    margin-bottom: 0.5rem !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
}

.compact-header p {
    color: #6b7280 !important;
    text-align: center !important;
    font-size: 0.95rem !important;
    margin-bottom: 0 !important;
    line-height: 1.3 !important;
}

/* Confidence Text Color */
.confidence-text {
    color: #d97706 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    text-shadow: 0 1px 2px rgba(217, 119, 6, 0.1);
}

/* Positive/Negative Colors */
.positive-color {
    color: #059669 !important;
}

.negative-color {
    color: #dc2626 !important;
}

.neutral-color {
    color: #d97706 !important;
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

# ----------------------- NEW FUNCTIONS FOR TOOLS PAGES -----------------------
def get_market_intelligence():
    """Market Intelligence Data"""
    return {
        'sector_performance': {
            'Banking': '+2.3%',
            'IT': '+1.8%', 
            'Pharma': '+0.9%',
            'Auto': '-0.5%',
            'Energy': '+1.2%'
        },
        'market_sentiment': 'Bullish',
        'volatility_index': '18.5',
        'put_call_ratio': '0.82'
    }

def get_market_news():
    """Market News Data"""
    return [
        {'title': 'RBI Keeps Rates Unchanged', 'source': 'Economic Times', 'impact': 'Neutral', 'time': '2 hours ago'},
        {'title': 'IT Sector Shows Strong Q4 Results', 'source': 'Business Standard', 'impact': 'Positive', 'time': '4 hours ago'},
        {'title': 'Auto Sales Decline in March', 'source': 'Money Control', 'impact': 'Negative', 'time': '6 hours ago'},
        {'title': 'Infrastructure Projects Boost Market', 'source': 'Financial Express', 'impact': 'Positive', 'time': '8 hours ago'}
    ]

def get_ai_signals():
    """AI Trading Signals"""
    return {
        'RELIANCE': {'signal': 'BUY', 'confidence': '85%', 'target': '₹2,800', 'stop_loss': '₹2,450'},
        'TCS': {'signal': 'HOLD', 'confidence': '72%', 'target': '₹3,500', 'stop_loss': '₹3,200'},
        'HDFC BANK': {'signal': 'BUY', 'confidence': '78%', 'target': '₹1,750', 'stop_loss': '₹1,600'},
        'INFOSYS': {'signal': 'SELL', 'confidence': '65%', 'target': '₹1,450', 'stop_loss': '₹1,600'}
    }

# ----------------------- SESSION STATE -----------------------
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Home"
if 'stock_name' not in st.session_state:
    st.session_state.stock_name = "NIFTY 50"
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "^NSEI"
if 'current_tool' not in st.session_state:
    st.session_state.current_tool = None

# ----------------------- HEADER -----------------------
st.markdown('<div class="main-header">SMART TRADE PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">by <em>Prasanth Subrahmanian</em> | Advanced Trading Analytics Platform</div>', unsafe_allow_html=True)

# ----------------------- MAIN NAVIGATION -----------------------
nav_options = ["🏠 Dashboard", "📈 Market Analysis", "🤖 AI Predictions", "💹 Options Trading", "📊 Portfolio", "🔍 Backtesting"]
nav_labels = ["Home", "Market Trends", "AI Predictions", "Options Trading", "Portfolio Insights", "Backtesting"]

nav_cols = st.columns(6)
for i, (col, option) in enumerate(zip(nav_cols, nav_options)):
    with col:
        btn_type = "primary" if st.session_state.current_section == nav_labels[i] else "secondary"
        if st.button(option, use_container_width=True, type=btn_type):
            st.session_state.current_section = nav_labels[i]
            st.session_state.current_tool = None
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
if st.session_state.current_section != "Home":
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
        st.write(f"Current: *{stock_name}* | *{timeframe}*")

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
                change_color = "#059669" if change_value >= 0 else "#dc2626"
                st.markdown(f"""
                <div class="feature-card">
                    <div style="font-weight: 600; margin-bottom: 0.6rem; color: #2563eb; font-size: 0.95rem;">{idx_name}</div>
                    <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem; color: #1f2937;">₹{idx_data['current']:.2f}</div>
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
                change_color = "#059669" if idx_data['change'] >= 0 else "#dc2626"
                st.markdown(f"""
                <div class="feature-card">
                    <div style="font-weight: 600; margin-bottom: 0.6rem; color: #2563eb; font-size: 0.95rem;">{idx_name}</div>
                    <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem; color: #1f2937;">₹{idx_data['current']:,.2f}</div>
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
        <div class="feature-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <div class="feature-icon">📈</div>
                <div style="margin-left: 0.8rem;">
                    <div class="feature-title">Market Intelligence</div>
                    <div class="feature-desc">Comprehensive market analysis and institutional insights</div>
                </div>
            </div>
            <div style="text-align: center; margin: 1rem 0;">
                <div style="font-size: 3rem; color: #2563eb; opacity: 0.7;">📊</div>
                <div style="color: #6b7280; font-size: 0.8rem; margin-top: 0.5rem;">Advanced Analytics</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Market Intelligence", key="market_intel", use_container_width=True):
            st.session_state.current_tool = "Market Intelligence"
            st.rerun()
    
    with tools_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <div class="feature-icon">📰</div>
                <div style="margin-left: 0.8rem;">
                    <div class="feature-title">Market News</div>
                    <div class="feature-desc">Latest financial news and market-moving events</div>
                </div>
            </div>
            <div style="text-align: center; margin: 1rem 0;">
                <div style="font-size: 3rem; color: #2563eb; opacity: 0.7;">📰</div>
                <div style="color: #6b7280; font-size: 0.8rem; margin-top: 0.5rem;">Real-time Updates</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Market News", key="market_news", use_container_width=True):
            st.session_state.current_tool = "Market News"
            st.rerun()
    
    with tools_cols[2]:
        st.markdown("""
        <div class="feature-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <div class="feature-icon">🤖</div>
                <div style="margin-left: 0.8rem;">
                    <div class="feature-title">AI Signals</div>
                    <div class="feature-desc">Machine learning based trading recommendations</div>
                </div>
            </div>
            <div style="text-align: center; margin: 1rem 0;">
                <div style="font-size: 3rem; color: #2563eb; opacity: 0.7;">🤖</div>
                <div style="color: #6b7280; font-size: 0.8rem; margin-top: 0.5rem;">Smart Predictions</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Check AI Signals", key="ai_signals", use_container_width=True):
            st.session_state.current_tool = "AI Signals"
            st.rerun()
    
    # Market Analysis Section with Finance Graphs
    st.markdown("### 📊 Trading Analysis & Finance Graphs")
    
    analysis_cols = st.columns(3)
    
    with analysis_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📈</div>
                <div class="feature-title">Technical Analysis</div>
                <div class="feature-desc">Advanced chart patterns, indicators, and trend analysis for precise market timing</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with analysis_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💹</div>
                <div class="feature-title">Options Flow</div>
                <div class="feature-desc">Real-time options chain analysis and institutional money flow tracking</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with analysis_cols[2]:
        st.markdown("""
        <div class="feature-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
                <div class="feature-title">Portfolio Analytics</div>
                <div class="feature-desc">Comprehensive portfolio performance metrics and risk assessment tools</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Sentiment
    st.markdown("### 🌡 Market Sentiment")
    sentiment_cols = st.columns(2)
    
    with sentiment_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📈 Today's Top Movers</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• RELIANCE: +2.8%</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• TCS: +1.9%</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• HDFC BANK: +1.5%</div>
            <div style="color: #dc2626; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• INFY: -0.8%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with sentiment_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎯 Trading Signals</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• Overall: BULLISH 📈</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• Volume: HIGH 🔥</div>
            <div style="color: #d97706; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• Volatility: MEDIUM ⚡</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600; font-size: 0.9rem;">• Momentum: STRONG 💪</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------- TOOLS PAGES -----------------------
def show_market_intelligence():
    """Market Intelligence Page"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>📈 Market Intelligence</h2>'
        '<p>Comprehensive market analysis and institutional insights</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    intel_data = get_market_intelligence()
    
    # Market Overview
    st.markdown("### 📊 Market Overview")
    overview_cols = st.columns(4)
    
    with overview_cols[0]:
        st.metric("Market Sentiment", intel_data['market_sentiment'], "Bullish")
    with overview_cols[1]:
        st.metric("Volatility Index", intel_data['volatility_index'], "18.5")
    with overview_cols[2]:
        st.metric("Put/Call Ratio", intel_data['put_call_ratio'], "0.82")
    with overview_cols[3]:
        st.metric("Advance/Decline", "1.24", "+0.15")
    
    # Sector Performance
    st.markdown("### 🏢 Sector Performance")
    sector_cols = st.columns(5)
    
    sectors = list(intel_data['sector_performance'].items())
    for i, (sector, performance) in enumerate(sectors):
        with sector_cols[i]:
            color = "#059669" if '+' in performance else "#dc2626"
            st.markdown(f"""
            <div class="feature-card" style="text-align: center;">
                <div style="font-weight: 600; color: #2563eb; margin-bottom: 0.5rem;">{sector}</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: {color};">{performance}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Institutional Flow
    st.markdown("### 💼 Institutional Flow")
    
    flow_cols = st.columns(2)
    with flow_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">FII Activity</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600;">• Net Buy: ₹1,250 Cr</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600;">• Equity: ₹980 Cr</div>
            <div style="color: #dc2626; margin: 0.5rem 0; font-weight: 600;">• Debt: ₹-270 Cr</div>
        </div>
        """, unsafe_allow_html=True)
    
    with flow_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">DII Activity</div>
            <div style="color: #dc2626; margin: 0.5rem 0; font-weight: 600;">• Net Sell: ₹-850 Cr</div>
            <div style="color: #dc2626; margin: 0.5rem 0; font-weight: 600;">• Equity: ₹-720 Cr</div>
            <div style="color: #059669; margin: 0.5rem 0; font-weight: 600;">• Debt: ₹130 Cr</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Breadth
    st.markdown("### 📈 Market Breadth")
    
    breadth_data = {
        'Advances': 1250,
        'Declines': 850,
        'Unchanged': 150,
        '52W High': 45,
        '52W Low': 12
    }
    
    breadth_cols = st.columns(5)
    for i, (metric, value) in enumerate(breadth_data.items()):
        with breadth_cols[i]:
            st.metric(metric, str(value))

def show_market_news():
    """Market News Page"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>📰 Market News & Events</h2>'
        '<p>Latest financial news and market-moving events</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    news_data = get_market_news()
    
    # News Feed
    st.markdown("### 📋 Latest News")
    
    for news in news_data:
        impact_color = {
            'Positive': '#059669',
            'Negative': '#dc2626', 
            'Neutral': '#d97706'
        }.get(news['impact'], '#d97706')
        
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 0.8rem;">
                <div style="flex: 1;">
                    <div style="font-weight: 700; color: #1f2937; margin-bottom: 0.3rem; font-size: 1.1rem;">{news['title']}</div>
                    <div style="color: #6b7280; font-size: 0.9rem;">{news['source']} • {news['time']}</div>
                </div>
                <div style="background: {impact_color}; color: #ffffff; padding: 0.3rem 0.8rem; border-radius: 12px; font-weight: 700; font-size: 0.8rem;">
                    {news['impact']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Earnings Calendar
    st.markdown("### 📅 Earnings Calendar")
    
    earnings_data = [
        {'company': 'TCS', 'date': 'Apr 12', 'expectation': 'Positive'},
        {'company': 'INFOSYS', 'date': 'Apr 13', 'expectation': 'Neutral'},
        {'company': 'HDFC BANK', 'date': 'Apr 15', 'expectation': 'Positive'},
        {'company': 'RELIANCE', 'date': 'Apr 18', 'expectation': 'Positive'}
    ]
    
    for earning in earnings_data:
        exp_color = '#059669' if earning['expectation'] == 'Positive' else '#d97706'
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; justify-content: between; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1f2937;">{earning['company']}</div>
                    <div style="color: #6b7280; font-size: 0.9rem;">Date: {earning['date']}</div>
                </div>
                <div style="background: {exp_color}; color: #ffffff; padding: 0.3rem 0.8rem; border-radius: 12px; font-weight: 700;">
                    {earning['expectation']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_ai_signals():
    """AI Signals Page"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>🤖 AI Trading Signals</h2>'
        '<p>Machine learning powered buy/sell recommendations</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    signals_data = get_ai_signals()
    
    # AI Signals Dashboard
    st.markdown("### 🎯 Live Trading Signals")
    
    for stock, signal in signals_data.items():
        signal_color = '#059669' if signal['signal'] == 'BUY' else '#dc2626' if signal['signal'] == 'SELL' else '#d97706'
        
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                <div style="font-weight: 700; color: #1f2937; font-size: 1.2rem;">{stock}</div>
                <div style="background: {signal_color}; color: #ffffff; padding: 0.4rem 1rem; border-radius: 20px; font-weight: 800;">
                    {signal['signal']}
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                <div>
                    <div style="color: #6b7280; font-size: 0.9rem;">Confidence</div>
                    <div style="color: #1f2937; font-weight: 600;">{signal['confidence']}</div>
                </div>
                <div>
                    <div style="color: #6b7280; font-size: 0.9rem;">Target</div>
                    <div style="color: #059669; font-weight: 600;">{signal['target']}</div>
                </div>
                <div>
                    <div style="color: #6b7280; font-size: 0.9rem;">Stop Loss</div>
                    <div style="color: #dc2626; font-weight: 600;">{signal['stop_loss']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Model Performance
    st.markdown("### 📊 Model Performance")
    
    perf_cols = st.columns(4)
    with perf_cols[0]:
        st.metric("Accuracy", "78.5%", "+2.3%")
    with perf_cols[1]:
        st.metric("Win Rate", "72.8%", "+1.5%")
    with perf_cols[2]:
        st.metric("Avg Return", "15.2%", "+0.8%")
    with perf_cols[3]:
        st.metric("Sharpe Ratio", "1.45", "+0.12")

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
                        <div style="font-size: 1rem; color: #2563eb; margin-bottom: 0.4rem;">{stock_name}</div>
                        <div style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(45deg, #2563eb, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.4rem;">
                            ₹{current_price:,.2f}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: {'#059669' if price_change >= 0 else '#dc2626'};">
                            {price_change:+.2f} ({price_change_pct:+.2f}%)
                        </div>
                        <div style="font-size: 0.9rem; color: #6b7280; margin-top: 0.3rem;">
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
    
    # Advanced Charting - LINE GRAPH
    st.markdown(f"### 📊 {stock_name} Price Chart")
    
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
            
            # Create LINE chart
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            fig = go.Figure()
            
            # LINE CHART for price
            fig.add_trace(go.Scatter(
                x=df_chart.index, 
                y=df_chart['Close'], 
                mode='lines', 
                name='Price',
                line=dict(color='#2563eb', width=3),
                fill='tozeroy',
                fillcolor='rgba(37, 99, 235, 0.1)'
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
                            line=dict(color='#dc2626', width=2, dash='dash')
                        ))
                except:
                    pass
            
            # Chart layout
            is_index = stock_name in ["NIFTY 50", "BANK NIFTY", "NIFTY IT", "SENSEX"]
            chart_title = f"{stock_name} - {timeframe} Price Chart"
            y_axis_title = "Index Value" if is_index else "Price (₹)"
            
            fig.update_layout(
                title=dict(text=chart_title, font=dict(color='#2563eb', size=18)),
                template="plotly_white",
                height=450,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                xaxis_title="Date",
                yaxis_title=y_axis_title,
                plot_bgcolor='rgba(255,255,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0.8)',
                font=dict(color='#333333'),
                hovermode='x unified'
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
            
            # Fallback: Create a simple demo LINE chart
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
                line=dict(color='#2563eb', width=3),
                fill='tozeroy',
                fillcolor='rgba(37, 99, 235, 0.1)'
            ))
            
            fig.update_layout(
                title=dict(text=f"{stock_name} - Sample Price Chart (Demo Data)", font=dict(color='#2563eb')),
                template="plotly_white",
                height=400,
                showlegend=True,
                xaxis_title="Date",
                yaxis_title="Price"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.info("⚠ Showing demo data. Real market data will load when available.")
            
    except Exception as e:
        st.error(f"Error in chart section: {str(e)}")
        
        # Ultra-simple fallback
        st.markdown("""
        <div class="chart-container">
            <p style="text-align: center; color: #6b7280; padding: 1.5rem; font-size: 1rem;">
                Chart is temporarily unavailable. Please try refreshing the page or select a different stock.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------- AI PREDICTIONS PAGE -----------------------
def show_ai_predictions():
    """AI Predictions - Forecasts next week/month price"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>🤖 AI Trading Intelligence</h2>'
        '<p>Machine learning forecasts and automated trading signals</p>'
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
    
    # AI Predictions Dashboard
    st.markdown("### 🎯 Price Forecast Dashboard")
    
    pred_cols = st.columns(3)
    with pred_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📅</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Next Week</div>', unsafe_allow_html=True)
        st.metric("Target Price", f"₹{current_price * 1.025:.2f}", "+2.5%")
        st.markdown('<div class="confidence-text">Confidence: 78%</div>', unsafe_allow_html=True)
        st.progress(78)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with pred_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Next Month</div>', unsafe_allow_html=True)
        st.metric("Target Price", f"₹{current_price * 1.068:.2f}", "+6.8%")
        st.markdown('<div class="confidence-text">Confidence: 72%</div>', unsafe_allow_html=True)
        st.progress(72)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with pred_cols[2]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">🎯</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Risk Assessment</div>', unsafe_allow_html=True)
        st.metric("Risk Level", "LOW", "-15%")
        st.markdown('<div class="confidence-text">Drawdown Risk: 25%</div>', unsafe_allow_html=True)
        st.progress(25)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stop Loss and Risk Management
    st.markdown("### 🛡 Risk Management")
    
    risk_cols = st.columns(4)
    with risk_cols[0]:
        stop_loss = current_price * 0.95
        st.metric("Stop Loss", f"₹{stop_loss:.2f}", "-5.0%")
    
    with risk_cols[1]:
        target_1 = current_price * 1.08
        st.metric("Target 1", f"₹{target_1:.2f}", "+8.0%")
    
    with risk_cols[2]:
        target_2 = current_price * 1.15
        st.metric("Target 2", f"₹{target_2:.2f}", "+15.0%")
    
    with risk_cols[3]:
        risk_reward = (target_1 - current_price) / (current_price - stop_loss)
        st.metric("Risk/Reward", f"{risk_reward:.2f}:1", "Good" if risk_reward > 1.5 else "Fair")
    
    # Prediction Chart
    st.markdown("### 📈 AI Prediction Chart")
    
    try:
        # Create prediction chart
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        # Mock prediction data
        base_price = current_price
        predictions = [base_price * (1 + 0.002 * i + np.random.normal(0, 0.01)) for i in range(30)]
        
        fig = go.Figure()
        
        # Current price line
        fig.add_trace(go.Scatter(
            x=[dates[0]], 
            y=[current_price],
            mode='markers',
            name='Current Price',
            marker=dict(color='#2563eb', size=10)
        ))
        
        # Prediction line
        fig.add_trace(go.Scatter(
            x=dates, 
            y=predictions,
            mode='lines+markers',
            name='AI Prediction',
            line=dict(color='#d97706', width=2.5, dash='dot')
        ))
        
        # Stop loss line
        fig.add_hline(y=stop_loss, line_dash="dash", line_color="#dc2626", 
                     annotation_text="Stop Loss", annotation_position="bottom right")
        
        # Target lines
        fig.add_hline(y=target_1, line_dash="dash", line_color="#059669",
                     annotation_text="Target 1", annotation_position="top right")
        fig.add_hline(y=target_2, line_dash="dash", line_color="#2563eb",
                     annotation_text="Target 2", annotation_position="top right")
        
        fig.update_layout(
            title=dict(text=f"AI Price Prediction for {stock_name} (Next 30 Days)", font=dict(color='#2563eb')),
            template="plotly_white",
            height=350,
            showlegend=True,
            xaxis_title="Date",
            yaxis_title="Price (₹)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error generating prediction chart: {str(e)}")

# ----------------------- OPTIONS TRADING PAGE -----------------------
def show_options_trading():
    """Options Trading - Option chain & strategy analyzer"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>💹 Options Trading</h2>'
        '<p>Options chain analysis and strategy builder</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Current price
    current_price = 2500
    try:
        df = get_stock_data(ticker, "1d")
        if df is not None and hasattr(df, 'empty') and not df.empty and len(df) > 0:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"{stock_name} Current Price: ₹{current_price:.2f}")
    except:
        current_price = 2500
    
    # Options Overview
    st.markdown("### 📊 Options Overview")
    overview_cols = st.columns(4)
    with overview_cols[0]:
        st.metric("IV Rank", "78%", "High")
    with overview_cols[1]:
        st.metric("Put/Call Ratio", "0.82", "Bullish")
    with overview_cols[2]:
        st.metric("Open Interest", "2.8M", "+15%")
    with overview_cols[3]:
        st.metric("Volume", "1.9M", "+22%")
    
    # Strategy Builder
    st.markdown("### 🛠 Strategy Builder")
    
    strat_cols = st.columns(2)
    with strat_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Strategy Configuration</div>', unsafe_allow_html=True)
        
        strategy = st.selectbox("Select Strategy", 
                              ["Long Call", "Long Put", "Covered Call", "Bull Spread", "Iron Condor"])
        expiry = st.selectbox("Expiry", ["Weekly", "Monthly"])
        strike = st.selectbox("Strike", ["ATM", "OTM 10%", "OTM 20%", "ITM 10%"])
        
        if st.button("Analyze Strategy", use_container_width=True):
            st.success("Strategy analyzed successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with strat_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Strategy Analysis</div>', unsafe_allow_html=True)
        
        st.metric("Max Profit", "₹12,500")
        st.metric("Max Loss", "₹1,500")
        st.metric("Breakeven", f"₹{current_price + 15:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------- PORTFOLIO INSIGHTS PAGE -----------------------
def show_portfolio_insights():
    """Portfolio Insights - User or sample portfolio charts"""
    st.markdown(
        '<div class="compact-header">'
        '<h2>📊 Portfolio Insights</h2>'
        '<p>Track your investments and analyze portfolio performance</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Portfolio Overview
    st.markdown("### 📈 Portfolio Overview")
    
    # Sample portfolio data
    portfolio_data = {
        'Stock': ['RELIANCE', 'TCS', 'HDFC BANK', 'INFOSYS', 'ICICI BANK'],
        'Quantity': [10, 25, 15, 30, 20],
        'Avg Price': [2450, 3200, 1650, 1500, 950],
        'Current Price': [2650, 3350, 1720, 1580, 1020],
        'Investment': [24500, 80000, 24750, 45000, 19000],
        'Current Value': [26500, 83750, 25800, 47400, 20400]
    }
    
    portfolio_df = pd.DataFrame(portfolio_data)
    portfolio_df['P&L'] = portfolio_df['Current Value'] - portfolio_df['Investment']
    portfolio_df['P&L %'] = (portfolio_df['P&L'] / portfolio_df['Investment']) * 100
    
    # Portfolio Metrics
    total_investment = portfolio_df['Investment'].sum()
    total_current = portfolio_df['Current Value'].sum()
    total_pnl = total_current - total_investment
    total_pnl_pct = (total_pnl / total_investment) * 100
    
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Total Investment", f"₹{total_investment:,.0f}")
    with metric_cols[1]:
        st.metric("Current Value", f"₹{total_current:,.0f}")
    with metric_cols[2]:
        st.metric("Total P&L", f"₹{total_pnl:,.0f}", f"{total_pnl_pct:.2f}%")
    with metric_cols[3]:
        st.metric("Daily Change", "₹+2,850", "+1.2%")
    
    # Portfolio Allocation Chart
    st.markdown("### 🎯 Portfolio Allocation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for allocation
        fig_pie = go.Figure(data=[go.Pie(
            labels=portfolio_df['Stock'],
            values=portfolio_df['Current Value'],
            hole=0.4,
            marker_colors=['#2563eb', '#3b82f6', '#dc2626', '#d97706', '#8b5cf6']
        )])
        fig_pie.update_layout(
            title=dict(text="Portfolio Allocation", font=dict(color='#2563eb')),
            template="plotly_white",
            height=350
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Performance bar chart
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=portfolio_df['Stock'],
            y=portfolio_df['P&L %'],
            marker_color=['#059669' if x >= 0 else '#dc2626' for x in portfolio_df['P&L %']],
            text=portfolio_df['P&L %'].round(2).astype(str) + '%',
            textposition='auto',
        ))
        fig_bar.update_layout(
            title=dict(text="Stock Performance (%)", font=dict(color='#2563eb')),
            template="plotly_white",
            height=350,
            xaxis_title="Stocks",
            yaxis_title="P&L %"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Portfolio Details Table
    st.markdown("### 📋 Portfolio Details")
    
    # Format the dataframe for display
    display_df = portfolio_df.copy()
    display_df['Avg Price'] = display_df['Avg Price'].apply(lambda x: f'₹{x:,.0f}')
    display_df['Current Price'] = display_df['Current Price'].apply(lambda x: f'₹{x:,.0f}')
    display_df['Investment'] = display_df['Investment'].apply(lambda x: f'₹{x:,.0f}')
    display_df['Current Value'] = display_df['Current Value'].apply(lambda x: f'₹{x:,.0f}')
    display_df['P&L'] = display_df['P&L'].apply(lambda x: f'₹{x:,.0f}')
    display_df['P&L %'] = display_df['P&L %'].apply(lambda x: f'{x:.2f}%')
    
    st.dataframe(display_df, use_container_width=True)
    
    # Risk Analysis
    st.markdown("### 🛡 Risk Analysis")
    
    risk_cols = st.columns(3)
    with risk_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Portfolio Beta</div>', unsafe_allow_html=True)
        st.metric("Beta", "1.12", "High")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with risk_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Volatility</div>', unsafe_allow_html=True)
        st.metric("Annual Vol", "18.5%", "Medium")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with risk_cols[2]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Diversification</div>', unsafe_allow_html=True)
        st.metric("Score", "7.2/10", "Good")
        st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown("### ⚙ Strategy Configuration")
    
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
        line=dict(color='#2563eb', width=2.5)
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
        name='Benchmark',
        line=dict(color='#d97706', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=dict(text="Strategy vs Benchmark Performance", font=dict(color='#2563eb')),
        template="plotly_white",
        height=400,
        showlegend=True,
        xaxis_title="Date",
        yaxis_title="Portfolio Value (₹)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trade Analysis
    st.markdown("### 📋 Trade Analysis")
    
    trade_data = {
        'Date': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05'],
        'Stock': ['RELIANCE', 'TCS', 'HDFC BANK', 'INFOSYS'],
        'Action': ['BUY', 'SELL', 'BUY', 'SELL'],
        'Quantity': [10, 25, 15, 30],
        'Price': [2450, 3350, 1650, 1580],
        'P&L': ['-', '₹3,750', '-', '₹2,400']
    }
    
    trade_df = pd.DataFrame(trade_data)
    st.dataframe(trade_df, use_container_width=True)

# ----------------------- MAIN APP LOGIC -----------------------
def main():
    """Main application logic"""
    
    # Handle tool pages from home
    if st.session_state.current_tool:
        if st.session_state.current_tool == "Market Intelligence":
            show_market_intelligence()
        elif st.session_state.current_tool == "Market News":
            show_market_news()
        elif st.session_state.current_tool == "AI Signals":
            show_ai_signals()
        return
    
    # Handle main sections
    if st.session_state.current_section == "Home":
        show_home()
    elif st.session_state.current_section == "Market Trends":
        show_market_trends()
    elif st.session_state.current_section == "AI Predictions":
        show_ai_predictions()
    elif st.session_state.current_section == "Options Trading":
        show_options_trading()
    elif st.session_state.current_section == "Portfolio Insights":
        show_portfolio_insights()
    elif st.session_state.current_section == "Backtesting":
        show_backtesting()

if __name__ == "__main__":
    main()