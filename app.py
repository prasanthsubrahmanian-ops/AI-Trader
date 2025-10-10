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
        stock = yf.Ticker(ticker)
        return stock.history(period=period)
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_daily_data(ticker, days=60):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=f"{days}d")
    except Exception as e:
        st.error(f"Error fetching daily data for {ticker}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_intraday_data(ticker, interval="5m", days=1):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=f"{days}d", interval=interval)
    except Exception as e:
        st.error(f"Error fetching intraday data for {ticker}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_market_data():
    """Get NIFTY, sector data with proper error handling"""
    indices = {
        'NIFTY 50': '^NSEI',
        'BANK NIFTY': '^NSEBANK', 
        'NIFTY IT': '^CNXIT',
        'SENSEX': '^BSESN'
    }
    
    data = {}
    for name, ticker in indices.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='2d')  # Get 2 days to calculate change
            
            if not hist.empty and len(hist) > 1:
                current_price = float(hist['Close'].iloc[-1])
                prev_price = float(hist['Close'].iloc[-2])
                change = current_price - prev_price
                change_pct = (change / prev_price) * 100
                
                data[name] = {
                    'current': current_price,
                    'change': change,
                    'change_pct': change_pct
                }
            else:
                # Fallback data
                data[name] = {
                    'current': 0.00,
                    'change': 0.00,
                    'change_pct': 0.00
                }
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            # Fallback data
            data[name] = {
                'current': 0.00,
                'change': 0.00, 
                'change_pct': 0.00
            }
    
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
st.markdown('<div class="main-header">SMART TRADE with Prasanth Subrahmanian</div>', unsafe_allow_html=True)

# ----------------------- MAIN NAVIGATION -----------------------
nav_options = ["🏠 Home", "📈 Market Trends", "🤖 AI Predictions", "💹 Options Trading", "📊 Portfolio Insights", "🔍 Backtesting"]
nav_labels = ["Home", "Market Trends", "AI Predictions", "Options Trading", "Portfolio Insights", "Backtesting"]

nav_cols = st.columns(6)
for i, (col, option) in enumerate(zip(nav_cols, nav_options)):
    with col:
        if st.button(option, use_container_width=True, 
                    type="primary" if st.session_state.current_section == nav_labels[i] else "secondary"):
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
        st.write(f"**Current:** {stock_name} | {timeframe}")

    st.session_state.stock_name = stock_name
    ticker = stocks[st.session_state.stock_name]
    st.session_state.current_ticker = ticker

section = st.session_state.current_section

# ----------------------- HOME PAGE -----------------------
def show_home_page():
    """Home page with overview and quick access"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;">'
        '<h2>🏠 Welcome to Smart Trade Analytics</h2>'
        '<p>Advanced trading tools and market analysis powered by AI</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Quick Stats with error handling
    st.markdown("### 📊 Market Overview")
    
    try:
        with st.spinner("Loading market data..."):
            market_data = get_market_data()
        
        cols = st.columns(4)
        indices = ['NIFTY 50', 'BANK NIFTY', 'NIFTY IT', 'SENSEX']
        
        for i, idx in enumerate(indices):
            with cols[i]:
                if idx in market_data and market_data[idx]['current'] > 0:
                    data = market_data[idx]
                    st.metric(
                        idx,
                        f"₹{data['current']:.2f}",
                        f"{data['change']:+.2f} ({data['change_pct']:+.2f}%)"
                    )
                else:
                    st.metric(idx, "Loading...", "0.00%")
    except Exception as e:
        st.error("Unable to load market data")
        # Show placeholder metrics
        cols = st.columns(4)
        indices = ['NIFTY 50', 'BANK NIFTY', 'NIFTY IT', 'SENSEX']
        for i, idx in enumerate(indices):
            with cols[i]:
                st.metric(idx, "₹0.00", "0.00%")
    
    # Feature Cards
    st.markdown("### 🚀 Trading Tools")
    
    features = [
        {
            "icon": "📈",
            "title": "Market Trends",
            "desc": "Real-time market indices, sector performance, and stock movers",
            "section": "Market Trends"
        },
        {
            "icon": "🤖", 
            "title": "AI Predictions",
            "desc": "Machine learning forecasts for next week and month prices",
            "section": "AI Predictions"
        },
        {
            "icon": "💹",
            "title": "Options Trading", 
            "desc": "Options chain analysis and strategy builder",
            "section": "Options Trading"
        },
        {
            "icon": "📊",
            "title": "Portfolio Insights",
            "desc": "Portfolio analysis and performance tracking",
            "section": "Portfolio Insights" 
        },
        {
            "icon": "🔍",
            "title": "Backtesting",
            "desc": "Test trading strategies on historical data",
            "section": "Backtesting"
        }
    ]
    
    # Display features in 2 columns
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <div class="feature-title">{feature['title']}</div>
                <div class="feature-desc">{feature['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Open {feature['title']}", key=f"home_{feature['section']}", use_container_width=True):
                st.session_state.current_section = feature['section']
                st.rerun()
    
    # Recent Activity
    st.markdown("### 📈 Recent Market Activity")
    
    activity_cols = st.columns(3)
    with activity_cols[0]:
        st.metric("Top Gainer", "RELIANCE", "+2.8%")
    with activity_cols[1]:
        st.metric("Top Loser", "TECHM", "-1.5%")
    with activity_cols[2]:
        st.metric("Volume Leader", "HDFC BANK", "25.4M")

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
    
    # Market Indices with better error handling
    st.markdown("### 📊 Market Indices")
    
    with st.spinner("Loading market data..."):
        market_data = get_market_data()
    
    if not market_data:
        st.error("Unable to fetch market data. Please check your internet connection.")
        return
    
    cols = st.columns(4)
    indices = ['NIFTY 50', 'BANK NIFTY', 'NIFTY IT', 'SENSEX']
    
    for i, idx in enumerate(indices):
        with cols[i]:
            if idx in market_data:
                data = market_data[idx]
                if data['current'] > 0:  # Valid data
                    st.metric(
                        idx,
                        f"₹{data['current']:.2f}",
                        f"{data['change']:+.2f} ({data['change_pct']:+.2f}%)"
                    )
                else:
                    st.metric(idx, "Loading...", "0.00%")
            else:
                st.metric(idx, "N/A", "0.00%")
    
    # Individual Stock Analysis
    st.markdown(f"### 🔍 {st.session_state.stock_name} Analysis")
    
    try:
        # Get stock data based on timeframe
        period_map = {
            "1D": "1d", 
            "1W": "5d", 
            "1M": "1mo", 
            "3M": "3mo", 
            "6M": "6mo", 
            "1Y": "1y"
        }
        
        df = get_stock_data(st.session_state.current_ticker, period_map.get(timeframe, "1mo"))
        
        if not df.empty and len(df) > 1:
            current_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2])
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100
            
            # Stock metrics
            st.markdown("#### Stock Overview")
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric("Current Price", f"₹{current_price:.2f}", 
                         f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
            with metric_cols[1]:
                st.metric("Day High", f"₹{df['High'].max():.2f}")
            with metric_cols[2]:
                st.metric("Day Low", f"₹{df['Low'].min():.2f}")
            with metric_cols[3]:
                volume = df['Volume'].iloc[-1] if 'Volume' in df.columns else 0
                st.metric("Volume", f"{volume:,.0f}")
            
            # Enhanced Price Chart
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="chart-header">{st.session_state.stock_name} - {timeframe} Price Chart</div>', unsafe_allow_html=True)
            
            # Create interactive chart with more features
            fig = go.Figure()
            
            # Candlestick chart for better visualization
            if len(df) > 10:  # Only show candlestick for sufficient data
                fig.add_trace(go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Price'
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=df.index, 
                    y=df['Close'], 
                    mode='lines', 
                    name='Close Price',
                    line=dict(color='#00ffcc', width=2)
                ))
            
            fig.update_layout(
                title=f"{st.session_state.stock_name} Price Movement",
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                template="plotly_dark",
                height=500,
                showlegend=True,
                font=dict(color="white")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.warning(f"No data available for {st.session_state.stock_name}. Please try another stock.")
            
    except Exception as e:
        st.error(f"Error loading chart data: {str(e)}")
        st.info("Please try selecting a different stock or timeframe.")
    
    # Enhanced Sector Performance
    st.markdown("### 🏢 Sector Performance")
    
    # Mock sector data (you can replace with real API calls)
    sectors = {
        "Banking": "+2.3%",
        "IT": "+1.8%", 
        "Pharma": "-0.5%",
        "Auto": "+1.2%",
        "FMCG": "+0.8%",
        "Energy": "+3.1%",
        "Real Estate": "+1.5%",
        "Metals": "-0.8%"
    }
    
    # Display sectors in a grid
    cols = st.columns(4)
    for i, (sector, performance) in enumerate(sectors.items()):
        with cols[i % 4]:
            color = "#00ffcc" if "+" in performance else "#ff4444"
            st.markdown(f"""
            <div class="feature-card" style="padding: 1rem; margin-bottom: 0.5rem;">
                <div style="font-weight: 600; margin-bottom: 0.3rem; font-size: 0.9rem;">{sector}</div>
                <div style="color: {color}; font-size: 1rem; font-weight: 600;">{performance}</div>
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
    try:
        df = get_daily_data(st.session_state.current_ticker, 30)
        if not df.empty and len(df) > 1:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
        else:
            current_price = 2500
            st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
    except:
        current_price = 2500
        st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
    
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
        {"name": "Neural Network", "accuracy": "79%", "icon": "🕸️"}
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
    try:
        df = get_daily_data(st.session_state.current_ticker, 1)
        if not df.empty and len(df) > 0:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
        else:
            current_price = 2500
            st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
    except:
        current_price = 2500
        st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
    
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
    st.markdown("### 🛠️ Strategy Builder")
    
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
        fig.update_layout(
            title="Profit & Loss",
            height=250, 
            template="plotly_dark", 
            showlegend=False,
            xaxis_title="Stock Price",
            yaxis_title="P&L (₹)"
        )
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
    fig.update_layout(
        template="plotly_dark", 
        height=400,
        title="Portfolio Allocation by Stock"
    )
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
    st.markdown("### ⚙️ Strategy Configuration")
    
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
        rsi_lower = st.slider("RSI Lower", 10,