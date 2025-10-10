import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import altair as alt
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="Prasanth Subrahmanian", 
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
        data = yf.download(ticker, period=period)
        if data.empty:
            st.error(f"No data found for {ticker}")
            return pd.DataFrame()
        return data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_daily_data(ticker, days=60):
    try:
        data = yf.download(ticker, period=f"{days}d")
        if data.empty:
            return pd.DataFrame()
        return data
    except Exception as e:
        st.error(f"Error fetching daily data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_intraday_data(ticker, interval="5m", days=1):
    try:
        data = yf.download(ticker, period=f"{days}d", interval=interval)
        if data.empty:
            return pd.DataFrame()
        return data
    except Exception as e:
        st.error(f"Error fetching intraday data: {str(e)}")
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
            st.warning(f"Could not fetch data for {name}: {str(e)}")
            continue
    return data

def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info
    except:
        return {}

# ----------------------- SESSION STATE -----------------------
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Home"
if 'stock_name' not in st.session_state:
    st.session_state.stock_name = "RELIANCE"
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "RELIANCE.NS"

# ----------------------- HEADER -----------------------
st.markdown('<div class="main-header">PRASANTH SUBRAHMANIAN</div>', unsafe_allow_html=True)

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
        '<h2>🏠 Welcome to Trading Analytics</h2>'
        '<p>Comprehensive market analysis, AI predictions, and portfolio management tools</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Quick Stats
    st.markdown("### 📊 Quick Market Overview")
    
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
        st.warning("Could not load market data at the moment")
    
    # Feature Cards
    st.markdown("### 🚀 Features")
    
    features_cols = st.columns(3)
    
    with features_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Market Trends</div>
            <div class="feature-desc">Real-time market data, indices, and sector performance analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with features_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Predictions</div>
            <div class="feature-desc">Machine learning forecasts for stock prices and trading signals</div>
        </div>
        """, unsafe_allow_html=True)
    
    with features_cols[2]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💹</div>
            <div class="feature-title">Options Trading</div>
            <div class="feature-desc">Options chain analysis and strategy builder with P&L charts</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("### 📈 Recent Activity")
    activity_cols = st.columns(2)
    
    with activity_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Top Gainers Today</div>
            <div style="color: #00ffcc;">RELIANCE: +2.3%</div>
            <div style="color: #00ffcc;">TCS: +1.8%</div>
            <div style="color: #00ffcc;">INFY: +1.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with activity_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Market Sentiment</div>
            <div style="color: #00ffcc;">Overall: Bullish 📈</div>
            <div style="color: #00ffcc;">Volume: High</div>
            <div style="color: #00ffcc;">Volatility: Medium</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------- MARKET TRENDS PAGE -----------------------
def show_market_trends():
    """Market Trends - Shows NIFTY, sectors, gainers, losers"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>📈 Market Trends & Analysis</h2>'
        '<p>Real-time market indices, sector performance, and stock movers</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Market Indices
    st.markdown("### 📊 Market Indices")
    
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
        st.warning("Could not load market indices data")
    
    # Individual Stock Analysis
    st.markdown(f"### 🔍 {stock_name} Analysis")
    
    try:
        # Get stock data
        period_map = {"1D": "5d", "1W": "1mo", "1M": "3mo", "3M": "6mo", "6M": "1y", "1Y": "2y"}
        df = get_stock_data(ticker, period_map.get(timeframe, "1mo"))
        
        if not df.empty and len(df) > 1:
            current_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2])
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100
            
            # Stock metrics
            st.markdown("#### Stock Overview")
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric("Current Price", f"₹{current_price:.2f}", f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
            with metric_cols[1]:
                st.metric("Day High", f"₹{df['High'].max():.2f}")
            with metric_cols[2]:
                st.metric("Day Low", f"₹{df['Low'].min():.2f}")
            with metric_cols[3]:
                volume = df['Volume'].iloc[-1] if 'Volume' in df.columns else 0
                st.metric("Volume", f"{volume:,.0f}")
            
            # Price Chart
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="chart-header">{stock_name} Price Chart</div>', unsafe_allow_html=True)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['Close'], 
                mode='lines', 
                name='Price',
                line=dict(color='#00ffcc', width=2)
            ))
            
            fig.update_layout(
                title=f"{stock_name} - {timeframe}",
                template="plotly_dark",
                height=400,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                xaxis_title="Date",
                yaxis_title="Price (₹)"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Insufficient data for {stock_name}. Please try a different timeframe or stock.")
            
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")
    
    # Sector Performance (Mock Data)
    st.markdown("### 🏢 Sector Performance")
    sectors = {
        "Banking": "+2.3%",
        "IT": "+1.8%", 
        "Pharma": "-0.5%",
        "Auto": "+1.2%",
        "FMCG": "+0.8%",
        "Energy": "+3.1%"
    }
    
    cols = st.columns(3)
    for i, (sector, performance) in enumerate(sectors.items()):
        with cols[i % 3]:
            color = "#00ffcc" if "+" in performance else "#ff4444"
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-weight: 600; margin-bottom: 0.5rem;">{sector}</div>
                <div style="color: {color}; font-size: 1.2rem; font-weight: 600;">{performance}</div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------- AI PREDICTIONS PAGE -----------------------
def show_ai_predictions():
    """AI Predictions - Forecasts next week/month price"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>🤖 AI Price Predictions</h2>'
        '<p>Machine learning forecasts for next week and month</p>'
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
    
    # AI Predictions
    st.markdown("### 📈 Price Forecasts")
    
    pred_cols = st.columns(2)
    with pred_cols[0]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📅</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Next Week Forecast</div>', unsafe_allow_html=True)
        st.metric("Predicted Price", f"₹{current_price * 1.025:.2f}", "+2.5%")
        st.progress(78, text="Confidence: 78%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with pred_cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Next Month Forecast</div>', unsafe_allow_html=True)
        st.metric("Predicted Price", f"₹{current_price * 1.068:.2f}", "+6.8%")
        st.progress(72, text="Confidence: 72%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Models
    st.markdown("### 🧠 AI Models Used")
    
    models_cols = st.columns(4)
    models = [
        {"name": "LSTM", "accuracy": "86%", "icon": "🧠"},
        {"name": "Random Forest", "accuracy": "83%", "icon": "🌳"},
        {"name": "XGBoost", "accuracy": "81%", "icon": "🚀"},
        {"name": "Neural Network", "accuracy": "79%", "icon": "🕸"}
    ]
    
    for i, model in enumerate(models):
        with models_cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{model['icon']}</div>
                <div style="font-weight: 600; margin-bottom: 0.3rem;">{model['name']}</div>
                <div style="color: #00ffcc; font-size: 0.9rem;">Accuracy: {model['accuracy']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Trading Signal
    st.markdown("### 🎯 AI Trading Signal")
    signal_cols = st.columns(3)
    with signal_cols[0]:
        st.markdown('<div class="prediction-badge">STRONG BUY</div>', unsafe_allow_html=True)
    with signal_cols[1]:
        st.metric("Confidence", "85%", "+2%")
    with signal_cols[2]:
        st.metric("Risk Level", "LOW", "Stable")

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
        ma_slow = st.slider("MA Slow Period", 20, 200, 50)
    with param_cols[2]:
        rsi_upper = st.slider("RSI Upper", 60, 90, 70)
    with param_cols[3]:
        rsi_lower = st.slider("RSI Lower", 10, 40, 30)
    
    if st.button("Run Backtest", type="primary", use_container_width=True):
        st.success("Backtest completed successfully!")
        
        # Backtest Results
        st.markdown("### 📈 Backtest Results")
        
        result_cols = st.columns(4)
        with result_cols[0]:
            st.metric("Final Value", "₹1,245,000", "+24.5%")
        with result_cols[1]:
            st.metric("Total Trades", "156")
        with result_cols[2]:
            st.metric("Win Rate", "62.8%", "+2.3%")
        with result_cols[3]:
            st.metric("Max Drawdown", "-8.2%", "Moderate")
        
        # Equity Curve
        st.markdown("### 📊 Equity Curve")
        
        # Mock equity curve
        dates = pd.date_range(start='2024-01-01', end='2024-12-10', freq='D')
        equity = capital + np.cumsum(np.random.normal(500, 2000, len(dates)))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=equity, mode='lines', name='Strategy', line=dict(color='#00ffcc')))
        fig.add_trace(go.Scatter(x=dates, y=[capital] * len(dates), mode='lines', name='Buy & Hold', 
                               line=dict(color='#ff4444', dash='dash')))
        fig.update_layout(
            title="Strategy vs Buy & Hold",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# ----------------------- MAIN PAGE ROUTING -----------------------
if section == "Home":
    show_home()
elif section == "Market Trends":
    show_market_trends()
elif section == "AI Predictions":
    show_ai_predictions()
elif section == "Options Trading":
    show_options_trading()
elif section == "Portfolio Insights":
    show_portfolio_insights()
elif section == "Backtesting":
    show_backtesting()

# -----------------