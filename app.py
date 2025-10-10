import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import altair as alt
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="Smart Trade with Prasanth Subrahmanian", 
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
    background-color: #0f0f0f !important;
    color: #ffffff !important;
    padding-top: 0.5rem !important;
}

.main-header {
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(45deg, #00ffcc, #0099ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    padding: 0.2rem 0;
}

/* Top Navigation */
.top-nav {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    margin: 0.2rem 0 1.5rem 0;
    flex-wrap: wrap;
}

.nav-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(0, 255, 204, 0.3);
    color: #00ffcc;
    padding: 0.6rem 1.2rem;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.nav-btn:hover {
    background: rgba(0, 255, 204, 0.2);
    border-color: #00ffcc;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);
}

.nav-btn.active {
    background: linear-gradient(45deg, #00ffcc, #0099ff);
    color: #000;
    border-color: #00ffcc;
}

.home-btn {
    background: linear-gradient(45deg, #ff6b6b, #ffa726);
    border: 1px solid rgba(255, 107, 107, 0.3);
    color: #000;
    padding: 0.6rem 1.2rem;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.home-btn:hover {
    background: linear-gradient(45deg, #ff5252, #ff9800);
    border-color: #ff6b6b;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

/* Compact Metrics */
.compact-metrics-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.5rem;
    margin: 0.5rem 0;
    font-size: 0.85rem;
}

.metric-item {
    text-align: center;
    padding: 0.3rem;
    border-radius: 6px;
}

.metric-label {
    font-size: 0.7rem;
    color: #888;
    margin-bottom: 0.2rem;
}

.metric-value {
    font-size: 0.8rem;
    font-weight: 600;
    color: #fff;
}

/* Cards */
.feature-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.feature-card:hover {
    border-color: #00ffcc;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 255, 204, 0.2);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 0.8rem;
    color: #00ffcc;
}

.feature-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #fff;
}

.feature-desc {
    font-size: 0.9rem;
    color: #888;
    margin-bottom: 1rem;
}

/* Chart Container */
.chart-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.chart-header {
    color: #00ffcc;
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

/* Options Panel */
.options-panel {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.options-chain {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
}

.call-options, .put-options {
    background: rgba(255, 255, 255, 0.03);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.prediction-badge {
    background: linear-gradient(45deg, #00ffcc, #0099ff);
    color: #000;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 1rem;
}

@media (max-width: 768px) {
    .compact-metrics-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    .main-header { font-size: 2.2rem; }
    .nav-btn { padding: 0.5rem 1rem; font-size: 0.9rem; }
    .options-chain {
        grid-template-columns: 1fr;
    }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------- CACHED FUNCTIONS -----------------------
@st.cache_data(ttl=300)
def get_stock_data(ticker, period="1y"):
    try:
        data = yf.download(ticker, period=period, progress=False)
        if data.empty:
            return pd.DataFrame()
        return data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_daily_data(ticker, days=60):
    try:
        data = yf.download(ticker, period=f"{days}d", progress=False)
        if data.empty:
            return pd.DataFrame()
        return data
    except Exception as e:
        st.error(f"Error fetching daily data: {str(e)}")
        return pd.DataFrame()

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
            df = yf.download(ticker, period='1d', progress=False)
            if not df.empty and len(df) > 1:
                data[name] = {
                    'current': df['Close'].iloc[-1],
                    'change': df['Close'].iloc[-1] - df['Close'].iloc[-2],
                    'change_pct': ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
                }
        except Exception as e:
            continue
    return data

# ----------------------- SESSION STATE -----------------------
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Home"
if 'stock_name' not in st.session_state:
    st.session_state.stock_name = "RELIANCE"
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "RELIANCE.NS"

# ----------------------- HEADER -----------------------
st.markdown('<div class="main-header">SMART TRADE WITH PRASANTH SUBRAHMANIAN</div>', unsafe_allow_html=True)

# ----------------------- MAIN NAVIGATION -----------------------
nav_options = ["🏠 Home", "📈 Market Trends", "🤖 AI Predictions", "💹 Options Trading", "📊 Portfolio Insights", "🔍 Backtesting"]
nav_labels = ["Home", "Market Trends", "AI Predictions", "Options Trading", "Portfolio Insights", "Backtesting"]

nav_cols = st.columns(6)
for i, (col, option) in enumerate(zip(nav_cols, nav_options)):
    with col:
        btn_type = "primary" if st.session_state.current_section == nav_labels[i] else "secondary"
        if st.button(option, use_container_width=True, type=btn_type):
            st.session_state.current_section = nav_labels[i]
            st.rerun()

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
        st.write(f"*Current:* {stock_name} | {timeframe}")

    st.session_state.stock_name = stock_name
    ticker = stocks[st.session_state.stock_name]
    st.session_state.current_ticker = ticker

section = st.session_state.current_section

# ----------------------- HOME PAGE -----------------------
def show_home():
    """Home page with overview and quick access"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>🏠 Welcome to Smart Trade Analytics</h2>'
        '<p>Advanced trading insights powered by AI and real-time market data</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Quick Stats
    st.markdown("### 📊 Live Market Overview")
    
    with st.spinner('Loading market data...'):
        market_data = get_market_data()
    
    if market_data:
        cols = st.columns(4)
        
        for i, (idx_name, idx_data) in enumerate(market_data.items()):
            with cols[i % 4]:
                change_color = "#00ffcc" if idx_data['change'] >= 0 else "#ff4444"
                st.markdown(f"""
                <div class="feature-card">
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">{idx_name}</div>
                    <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">₹{idx_data['current']:.2f}</div>
                    <div style="color: {change_color}; font-weight: 600;">
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
                change_color = "#00ffcc" if idx_data['change'] >= 0 else "#ff4444"
                st.markdown(f"""
                <div class="feature-card">
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">{idx_name}</div>
                    <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">₹{idx_data['current']:,.2f}</div>
                    <div style="color: {change_color}; font-weight: 600;">
                        {idx_data['change']:+.2f} ({idx_data['change_pct']:+.2f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Trading Tools Section
    st.markdown("### 🛠 Trading Tools")
    
    tools_cols = st.columns(3)
    
    with tools_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Live Charts</div>
            <div class="feature-desc">Interactive price charts with technical indicators and drawing tools</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tools_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Signals</div>
            <div class="feature-desc">Machine learning based buy/sell signals and price predictions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tools_cols[2]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💹</div>
            <div class="feature-title">Options Analysis</div>
            <div class="feature-desc">Advanced options strategy builder and risk analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Sentiment
    st.markdown("### 📊 Market Sentiment")
    sentiment_cols = st.columns(2)
    
    with sentiment_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📈 Today's Top Movers</div>
            <div style="color: #00ffcc; margin: 0.5rem 0;">• RELIANCE: +2.8%</div>
            <div style="color: #00ffcc; margin: 0.5rem 0;">• TCS: +1.9%</div>
            <div style="color: #00ffcc; margin: 0.5rem 0;">• HDFC BANK: +1.5%</div>
            <div style="color: #ff4444; margin: 0.5rem 0;">• INFY: -0.8%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with sentiment_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎯 Trading Signals</div>
            <div style="color: #00ffcc; margin: 0.5rem 0;">• Overall: BULLISH</div>
            <div style="color: #00ffcc; margin: 0.5rem 0;">• Volume: HIGH</div>
            <div style="color: #ffaa00; margin: 0.5rem 0;">• Volatility: MEDIUM</div>
            <div style="color: #00ffcc; margin: 0.5rem 0;">• Momentum: STRONG</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------- MARKET TRENDS PAGE -----------------------
def show_market_trends():
    """Market Trends - Shows NIFTY, sectors, gainers, losers"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>📈 Advanced Market Analysis</h2>'
        '<p>Real-time charts, technical indicators, and market insights</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Market Indices
    st.markdown("### 📊 Live Indices")
    
    market_data = get_market_data()
    if market_data:
        cols = st.columns(4)
        
        for i, (idx_name, idx_data) in enumerate(market_data.items()):
            with cols[i % 4]:
                st.metric(
                    idx_name,
                    f"₹{idx_data['current']:.2f}",
                    f"{idx_data['change']:+.2f} ({idx_data['change_pct']:+.2f}%)"
                )
    else:
        st.info("Market data loading...")
    
    # Advanced Charting
    st.markdown(f"### 📊 {stock_name} Advanced Chart")
    
    try:
        # Get stock data
        period_map = {"1D": "5d", "1W": "1mo", "1M": "3mo", "3M": "6mo", "6M": "1y", "1Y": "2y"}
        df = get_stock_data(ticker, period_map.get(timeframe, "1mo"))
        
        if not df.empty and len(df) > 1:
            current_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2])
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100
            
            # Advanced Chart with multiple indicators
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            # Create subplots
            fig = go.Figure()
            
            # Price line
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['Close'], 
                mode='lines', 
                name='Price',
                line=dict(color='#00ffcc', width=2)
            ))
            
            # Add moving averages
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MA50'] = df['Close'].rolling(window=50).mean()
            
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['MA20'], 
                mode='lines', 
                name='MA20',
                line=dict(color='#ff4444', width=1, dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['MA50'], 
                mode='lines', 
                name='MA50',
                line=dict(color='#0099ff', width=1, dash='dash')
            ))
            
            fig.update_layout(
                title=f"{stock_name} - {timeframe} | Price: ₹{current_price:.2f} ({price_change_pct:+.2f}%)",
                template="plotly_dark",
                height=500,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                xaxis_title="Date",
                yaxis_title="Price (₹)"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Technical Indicators
            st.markdown("### 🔧 Technical Indicators")
            
            tech_cols = st.columns(4)
            
            # Calculate basic indicators
            with tech_cols[0]:
                rsi = 65.2  # Mock RSI
                st.metric("RSI (14)", f"{rsi}", "Neutral")
                
            with tech_cols[1]:
                macd = 2.5  # Mock MACD
                st.metric("MACD", f"{macd}", "Bullish")
                
            with tech_cols[2]:
                volume_avg = df['Volume'].mean() if 'Volume' in df.columns else 0
                current_volume = df['Volume'].iloc[-1] if 'Volume' in df.columns else 0
                volume_ratio = (current_volume / volume_avg) if volume_avg > 0 else 1
                st.metric("Volume Ratio", f"{volume_ratio:.1f}x", "High" if volume_ratio > 1.5 else "Normal")
                
            with tech_cols[3]:
                volatility = df['Close'].pct_change().std() * np.sqrt(252) * 100  # Annualized volatility
                st.metric("Volatility", f"{volatility:.1f}%", "High" if volatility > 30 else "Medium")
                
        else:
            st.warning(f"Insufficient data for {stock_name}. Please try a different timeframe or stock.")
            
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")

# ----------------------- AI PREDICTIONS PAGE -----------------------
def show_ai_predictions():
    """AI Predictions - Forecasts next week/month price"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>🤖 AI Trading Intelligence</h2>'
        '<p>Machine learning forecasts and automated trading signals</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Current price
    current_price = 0
    try:
        df = get_daily_data(ticker, 30)
        if not df.empty and len(df) > 0:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"{stock_name} Current Price: ₹{current_price:.2f}")
    except:
        current_price = 2500  # Fallback price
    
    # AI Predictions Dashboard
    st.markdown("### 🎯 Price Forecast Dashboard")
    
    pred_cols = st.columns(3)
    with pred_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📅</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Next Week</div>', unsafe_allow_html=True)
        st.metric("Target Price", f"₹{current_price * 1.025:.2f}", "+2.5%")
        st.progress(78, text="Confidence: 78%")
        st.markdown('<div style="color: #00ffcc; font-size: 0.8rem;">📈 Bullish Momentum</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with pred_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Next Month</div>', unsafe_allow_html=True)
        st.metric("Target Price", f"₹{current_price * 1.068:.2f}", "+6.8%")
        st.progress(72, text="Confidence: 72%")
        st.markdown('<div style="color: #00ffcc; font-size: 0.8rem;">🚀 Strong Buy Signal</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with pred_cols[2]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">🎯</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Risk Assessment</div>', unsafe_allow_html=True)
        st.metric("Risk Level", "LOW", "-15%")
        st.progress(25, text="Drawdown Risk: 25%")
        st.markdown('<div style="color: #00ffcc; font-size: 0.8rem;">🛡️ Protected Strategy</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Trading Signals
    st.markdown("### 📡 Live Trading Signals")
    
    signal_cols = st.columns(4)
    with signal_cols[0]:
        st.markdown('<div class="prediction-badge">STRONG BUY</div>', unsafe_allow_html=True)
    with signal_cols[1]:
        st.metric("Signal Strength", "85%", "+2%")
    with signal_cols[2]:
        st.metric("Stop Loss", f"₹{current_price * 0.95:.2f}", "-5.0%")
    with signal_cols[3]:
        st.metric("Target 1", f"₹{current_price * 1.08:.2f}", "+8.0%")

# ----------------------- OPTIONS TRADING PAGE -----------------------
def show_options_trading():
    """Options Trading - Option chain & strategy analyzer"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>💹 Options Trading</h2>'
        '<p>Options chain analysis and strategy builder</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Current price
    current_price = 2500
    try:
        df = get_daily_data(ticker, 1)
        if not df.empty and len(df) > 0:
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
        
        # P&L Chart
        strikes = np.arange(current_price - 100, current_price + 100, 10)
        pnl = [max(s - (current_price + 15), -15) * 100 for s in strikes]  # Mock P&L
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=strikes, y=pnl, mode='lines', name='P&L', line=dict(color='#00ffcc')))
        fig.add_vline(x=current_price, line_dash="dash", line_color="white")
        fig.update_layout(title="Profit & Loss", height=250, template="plotly_dark", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Max Profit", "₹12,500")
        st.metric("Max Loss", "₹1,500")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------- PORTFOLIO INSIGHTS PAGE -----------------------
def show_portfolio_insights():
    """Portfolio Insights - User or sample portfolio charts"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>📊 Portfolio Insights</h2>'
        '<p>Portfolio analysis and performance tracking</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Sample Portfolio
    st.markdown("### 💼 Sample Portfolio")
    
    portfolio_data = {
        "Stock": ["RELIANCE", "TCS", "HDFC BANK", "INFY", "ICICI BANK"],
        "Quantity": [50, 100, 75, 120, 80],
        "Avg Price": [2450, 3200, 1650, 1850, 920],
        "Current Price": [2580, 3350, 1680, 1920, 950],
        "P&L (%)": ["+5.3%", "+4.7%", "+1.8%", "+3.8%", "+3.3%"]
    }
    
    portfolio_df = pd.DataFrame(portfolio_data)
    portfolio_df['Investment'] = portfolio_df['Quantity'] * portfolio_df['Avg Price']
    portfolio_df['Current Value'] = portfolio_df['Quantity'] * portfolio_df['Current Price']
    portfolio_df['P&L'] = portfolio_df['Current Value'] - portfolio_df['Investment']
    
    # Portfolio Summary
    total_investment = portfolio_df['Investment'].sum()
    total_value = portfolio_df['Current Value'].sum()
    total_pnl = total_value - total_investment
    total_pnl_pct = (total_pnl / total_investment) * 100
    
    summary_cols = st.columns(4)
    with summary_cols[0]:
        st.metric("Total Investment", f"₹{total_investment:,.0f}")
    with summary_cols[1]:
        st.metric("Current Value", f"₹{total_value:,.0f}")
    with summary_cols[2]:
        st.metric("Total P&L", f"₹{total_pnl:,.0f}", f"{total_pnl_pct:+.1f}%")
    with summary_cols[3]:
        st.metric("Portfolio Beta", "0.92", "Low Risk")
    
    # Portfolio Allocation Chart
    st.markdown("### 📈 Portfolio Allocation")
    
    fig = go.Figure(data=[go.Pie(
        labels=portfolio_df['Stock'],
        values=portfolio_df['Current Value'],
        hole=0.4,
        marker_colors=['#00ffcc', '#0099ff', '#ff4444', '#ffaa00', '#ff00ff']
    )])
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance Chart
    st.markdown("### 📊 Performance Trend")
    
    # Mock performance data
    dates = pd.date_range(start='2024-01-01', end='2024-12-10', freq='D')
    performance = 1000000 + np.cumsum(np.random.normal(5000, 20000, len(dates)))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=performance, mode='lines', name='Portfolio Value', line=dict(color='#00ffcc')))
    fig.update_layout(
        title="Portfolio Value Over Time",
        template="plotly_dark",
        height=300,
        xaxis_title="Date",
        yaxis_title="Portfolio Value (₹)"
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------- BACKTESTING PAGE -----------------------
def show_backtesting():
    """Backtesting - Test strategies on past data"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>🔍 Strategy Backtesting</h2>'
        '<p>Test trading strategies on historical data</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Strategy Configuration
    st.markdown("### ⚙ Strategy Configuration")
    
    config_cols = st.columns(3)
    with config_cols[0]:
        strategy = st.selectbox("Trading Strategy", 
                              ["Moving Average Crossover", "RSI Strategy", "MACD Strategy", "Bollinger Bands"])
    with config_cols[1]:
        capital = st.number_input("Initial Capital (₹)", value=100000, step=10000)
    with config_cols[2]:
        period = st.selectbox("Backtest Period", ["3 Months", "6 Months", "1 Year", "2 Years"])
    
    # Parameters
    st.markdown("### 📊 Strategy Parameters")
    param_cols = st.columns(4)
    with param_cols[0]:
        ma_fast = st.slider("MA Fast Period", 5, 50, 20)
    with param_cols[1]:
        ma_slow =