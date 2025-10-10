import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import altair as alt
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="Smart Trade Analytics", 
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
.compact-metrics {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.8rem;
    margin: 1rem 0;
}

.metric-box {
    background: rgba(255, 255, 255, 0.05);
    padding: 0.8rem;
    border-radius: 10px;
    border-left: 3px solid #00ffcc;
    text-align: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.metric-label {
    font-size: 0.75rem;
    color: #888;
    margin-bottom: 0.3rem;
}

.metric-value {
    font-size: 0.9rem;
    font-weight: 600;
    color: #fff;
}

.metric-change {
    font-size: 0.7rem;
    color: #00ffcc;
}

.metric-change.negative {
    color: #ff4444;
}

/* Research Cards */
.research-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.research-card:hover {
    border-color: #00ffcc;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 255, 204, 0.2);
}

.research-icon {
    font-size: 2rem;
    margin-bottom: 0.8rem;
    color: #00ffcc;
}

.research-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #fff;
}

.research-desc {
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

/* AI Prediction Cards */
.ai-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
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
    .compact-metrics {
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
    return yf.download(ticker, period=period)

@st.cache_data(ttl=300)
def get_daily_data(ticker, days=60):
    return yf.download(ticker, period=f"{days}d")

@st.cache_data(ttl=300)
def get_intraday_data(ticker, interval="5m", days=1):
    return yf.download(ticker, period=f"{days}d", interval=interval)

@st.cache_data(ttl=300)
def get_weekly_data(ticker, period="6mo"):
    return yf.download(ticker, period=period, interval="1wk")

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
if 'chart_period' not in st.session_state:
    st.session_state.chart_period = "1D"
if 'current_report' not in st.session_state:
    st.session_state.current_report = None
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "RELIANCE.NS"
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = "Candlestick"

# ----------------------- HEADER -----------------------
st.markdown('<div class="main-header">SMART TRADE ANALYTICS</div>', unsafe_allow_html=True)

# ----------------------- ENHANCED NAVIGATION -----------------------
nav_options = ["🏠 Home", "📊 Charts", "📑 Research", "💹 Options", "🤖 AI Predictions"]
nav_labels = [option.split(" ")[-1] for option in nav_options]

nav_cols = st.columns(5)
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

# Stock selection available on all pages
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    stock_name = st.selectbox("Select Stock", list(stocks.keys()), 
                             index=list(stocks.keys()).index(st.session_state.stock_name))
with col2:
    if st.session_state.current_section == "Charts":
        chart_period = st.selectbox("Timeframe", 
                                   ["1D", "1W", "1M", "3M", "6M", "1Y", "2Y", "5Y"],
                                   index=0)
    else:
        chart_period = st.selectbox("Timeframe", 
                                   ["1D", "1W", "1M", "3M", "6M", "1Y"],
                                   index=2)
with col3:
    st.write("")
    st.write(f"**Current:** {stock_name} | {chart_period}")

st.session_state.stock_name = stock_name
st.session_state.chart_period = chart_period

# Always update ticker based on selected stock
ticker = stocks[st.session_state.stock_name]
st.session_state.current_ticker = ticker
section = st.session_state.current_section

# ----------------------- CHARTING FUNCTIONS -----------------------
def create_interactive_chart(df, chart_type="Candlestick", title="Price Chart"):
    """Create interactive charts using Plotly"""
    
    if chart_type == "Candlestick":
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='#00ffcc',
            decreasing_line_color='#ff4444',
            name='Price'
        )])
        
    elif chart_type == "Line":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#00ffcc', width=2)
        ))
    
    elif chart_type == "Area":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Close'],
            fill='tozeroy',
            mode='none',
            name='Close Price',
            fillcolor='rgba(0, 255, 204, 0.3)',
            line=dict(color='#00ffcc')
        ))
    
    # Add moving averages
    if len(df) > 20:
        df['SMA_20'] = df['Close'].rolling(20).mean()
        df['SMA_50'] = df['Close'].rolling(50).mean()
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['SMA_20'],
            mode='lines',
            name='SMA 20',
            line=dict(color='#ffaa00', width=1, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['SMA_50'],
            mode='lines',
            name='SMA 50',
            line=dict(color='#ff00ff', width=1, dash='dash')
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        template="plotly_dark",
        height=500,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        font=dict(color="white"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def show_charts_page():
    """Enhanced charts page with 1D, weekly charts and multiple timeframes"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;"><h2>📊 Advanced Chart Analysis</h2><p>Interactive charts with multiple timeframes and technical indicators</p></div>',
        unsafe_allow_html=True,
    )
    
    # Chart type and timeframe selection
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        chart_type = st.selectbox("Chart Type", 
                                 ["Candlestick", "Line", "Area"],
                                 index=0)
        st.session_state.chart_type = chart_type
    
    with col2:
        indicators = st.multiselect("Technical Indicators",
                                  ["SMA", "EMA", "RSI", "MACD", "Bollinger Bands"],
                                  default=["SMA"])
    
    with col3:
        st.info(f"**{st.session_state.stock_name}** | {st.session_state.chart_period} | {chart_type} Chart")
    
    # Get data based on selected period
    try:
        if st.session_state.chart_period == "1D":
            df = get_intraday_data(ticker, interval="5m", days=1)
            title = f"{st.session_state.stock_name} - 1 Day Chart (5min intervals)"
        elif st.session_state.chart_period == "1W":
            df = get_intraday_data(ticker, interval="15m", days=7)
            title = f"{st.session_state.stock_name} - 1 Week Chart (15min intervals)"
        elif st.session_state.chart_period == "1M":
            df = get_daily_data(ticker, days=30)
            title = f"{st.session_state.stock_name} - 1 Month Chart"
        elif st.session_state.chart_period == "3M":
            df = get_daily_data(ticker, days=90)
            title = f"{st.session_state.stock_name} - 3 Month Chart"
        elif st.session_state.chart_period == "6M":
            df = get_daily_data(ticker, days=180)
            title = f"{st.session_state.stock_name} - 6 Month Chart"
        else:
            period_map = {"1Y": "1y", "2Y": "2y", "5Y": "5y"}
            df = get_stock_data(ticker, period_map.get(st.session_state.chart_period, "1y"))
            title = f"{st.session_state.stock_name} - {st.session_state.chart_period} Chart"
        
        if df.empty:
            st.error("No data available. Try again later or choose another stock.")
            return
        
        # Display current price info
        current_price = float(df['Close'].iloc[-1])
        prev_price = float(df['Close'].iloc[-2]) if len(df) > 1 else current_price
        price_change = current_price - prev_price
        price_change_pct = (price_change / prev_price) * 100 if prev_price > 0 else 0
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Price", f"₹{current_price:.2f}", f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
        with col2:
            st.metric("Today High", f"₹{df['High'].max():.2f}")
        with col3:
            st.metric("Today Low", f"₹{df['Low'].min():.2f}")
        with col4:
            volume = df['Volume'].iloc[-1] if 'Volume' in df.columns else 0
            st.metric("Volume", f"{volume:,.0f}")
        
        # Main chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-header">{title}</div>', unsafe_allow_html=True)
        
        fig = create_interactive_chart(df, chart_type=chart_type, title=title)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional charts in tabs
        st.markdown("### Technical Analysis")
        tab1, tab2, tab3 = st.tabs(["📈 Indicators", "📊 Volume", "🎯 Patterns"])
        
        with tab1:
            # RSI Chart
            if len(df) > 14:
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(x=df.index, y=rsi, mode='lines', name='RSI', line=dict(color='#00ffcc')))
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                fig_rsi.update_layout(title="RSI (14)", height=300, template="plotly_dark")
                st.plotly_chart(fig_rsi, use_container_width=True)
        
        with tab2:
            # Volume chart
            if 'Volume' in df.columns:
                fig_volume = go.Figure()
                colors = ['#00ffcc' if close >= open else '#ff4444' 
                         for close, open in zip(df['Close'], df['Open'])]
                
                fig_volume.add_trace(go.Bar(
                    x=df.index,
                    y=df['Volume'],
                    marker_color=colors,
                    name='Volume'
                ))
                fig_volume.update_layout(title="Volume", height=300, template="plotly_dark")
                st.plotly_chart(fig_volume, use_container_width=True)
        
        with tab3:
            # Price patterns analysis
            st.info("**Pattern Recognition Analysis**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Trend", "Bullish", "Strong")
            with col2:
                st.metric("Support", f"₹{df['Low'].tail(10).min():.2f}", "Strong")
            with col3:
                st.metric("Resistance", f"₹{df['High'].tail(10).max():.2f}", "Moderate")
                
    except Exception as e:
        st.error(f"Error loading chart data: {str(e)}")

# ----------------------- RESEARCH REPORTS PAGE -----------------------
def show_research_reports():
    """Dedicated research reports page"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;"><h2>📑 Comprehensive Research Reports</h2><p>In-depth fundamental & technical analysis reports</p></div>',
        unsafe_allow_html=True,
    )
    
    # Current stock overview
    try:
        df = get_daily_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[-2])
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
            
            st.success(f"**{st.session_state.stock_name}: ₹{current_price:.2f} | {change:+.2f} ({change_pct:+.2f}%)**")
    except:
        pass
    
    # Research categories
    st.markdown("### 📋 Research Categories")
    
    categories = [
        {
            "name": "📊 Fundamental Analysis",
            "reports": [
                {"icon": "📈", "title": "Financial Statements", "desc": "Income, Balance Sheet, Cash Flow"},
                {"icon": "💰", "title": "Valuation Models", "desc": "DCF, Comparable Analysis"},
                {"icon": "🏢", "title": "Business Model", "desc": "Revenue streams & competitive advantage"},
                {"icon": "📊", "title": "Management Analysis", "desc": "Leadership & governance"}
            ]
        },
        {
            "name": "⚡ Technical Analysis", 
            "reports": [
                {"icon": "📉", "title": "Price Action", "desc": "Support, Resistance, Patterns"},
                {"icon": "📊", "title": "Indicator Analysis", "desc": "RSI, MACD, Moving Averages"},
                {"icon": "🎯", "title": "Price Targets", "desc": "Short, Medium & Long term targets"},
                {"icon": "🔄", "title": "Momentum Analysis", "desc": "Trend strength & reversals"}
            ]
        },
        {
            "name": "🌍 Market Intelligence",
            "reports": [
                {"icon": "📈", "title": "Industry Outlook", "desc": "Sector analysis & trends"},
                {"icon": "⚔️", "title": "Competitive Landscape", "desc": "Market position & peers"},
                {"icon": "🌐", "title": "Macro Analysis", "desc": "Economic factors impact"},
                {"icon": "📰", "title": "News Sentiment", "desc": "Media coverage analysis"}
            ]
        }
    ]
    
    # Display categories in tabs
    tabs = st.tabs([category["name"] for category in categories])
    
    for i, (tab, category) in enumerate(zip(tabs, categories)):
        with tab:
            cols = st.columns(2)
            for idx, report in enumerate(category["reports"]):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="research-card">
                        <div class="research-icon">{report['icon']}</div>
                        <div class="research-title">{report['title']}</div>
                        <div class="research-desc">{report['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Generate Report", key=f"{report['title']}_{i}", use_container_width=True):
                        st.session_state.current_report = report['title']
                        st.rerun()
    
    # Recent Reports
    st.markdown("### 📄 Recent Research Reports")
    recent_reports = [
        {"title": "Q3 FY2024 Earnings Analysis", "date": "2024-01-15", "rating": "BUY", "target": "₹2,850"},
        {"title": "Technical Breakout Analysis", "date": "2024-01-10", "rating": "STRONG BUY", "target": "₹2,950"},
        {"title": "Industry Position Update", "date": "2024-01-05", "rating": "HOLD", "target": "₹2,600"}
    ]
    
    for report in recent_reports:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{report['title']}**")
        with col2:
            st.write(f"Rating: **{report['rating']}**")
        with col3:
            st.write(f"Target: **{report['target']}**")
        st.progress(75 if report['rating'] == 'BUY' else 90 if report['rating'] == 'STRONG BUY' else 50)

# ----------------------- OPTIONS TRADING PAGE -----------------------
def show_options_trading():
    """Dedicated options trading page"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;"><h2>💹 Advanced Options Trading</h2><p>Options chain analysis, strategy builder, and risk management</p></div>',
        unsafe_allow_html=True,
    )
    
    # Current market data
    try:
        df = get_daily_data(ticker, 1)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
    except:
        current_price = 0
    
    # Options dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("IV Rank", "78%", "High", delta_color="inverse")
    with col2:
        st.metric("Put/Call Ratio", "0.75", "Bullish")
    with col3:
        st.metric("Open Interest", "3.2M", "+22%")
    with col4:
        st.metric("Volume", "2.1M", "+18%")
    
    # Options strategy builder
    st.markdown("### 🛠️ Options Strategy Builder")
    
    strategy_col1, strategy_col2 = st.columns([1, 2])
    
    with strategy_col1:
        st.subheader("Strategy Configuration")
        strategy_type = st.selectbox("Strategy Type", 
                                   ["Long Call", "Long Put", "Covered Call", "Cash Secured Put", 
                                    "Bull Call Spread", "Bear Put Spread", "Iron Condor", "Strangle"])
        
        expiry = st.selectbox("Expiry Date", ["Weekly", "Monthly", "Quarterly"])
        strike_type = st.selectbox("Strike Selection", ["ATM", "OTM 10%", "OTM 20%", "ITM 10%", "Custom"])
        
        quantity = st.slider("Contracts", 1, 100, 10)
        premium = st.number_input("Premium per contract", min_value=0.0, value=15.0, step=0.5)
        
        if st.button("Analyze Strategy", type="primary", use_container_width=True):
            st.success(f"**{strategy_type}** strategy analyzed!")
    
    with strategy_col2:
        st.markdown('<div class="options-panel">', unsafe_allow_html=True)
        st.subheader("Strategy Analysis & P&L")
        
        # P&L Chart
        strikes = np.arange(current_price - 100, current_price + 100, 10)
        pnl = []
        
        for strike in strikes:
            if strategy_type == "Long Call":
                pnl.append(max(strike - (current_price + premium), -premium) * quantity * 100)
            elif strategy_type == "Long Put":
                pnl.append(max((current_price - premium) - strike, -premium) * quantity * 100)
            else:
                pnl.append((strike - current_price) * quantity * 100)
        
        fig_pnl = go.Figure()
        fig_pnl.add_trace(go.Scatter(x=strikes, y=pnl, mode='lines', name='P&L', line=dict(color='#00ffcc')))
        fig_pnl.add_vline(x=current_price, line_dash="dash", line_color="white", annotation_text="Current Price")
        fig_pnl.update_layout(title="Profit & Loss Analysis", height=300, template="plotly_dark")
        st.plotly_chart(fig_pnl, use_container_width=True)
        
        # Risk metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Max Profit", "₹12,500", "Unlimited" if "Call" in strategy_type else "Limited")
        with col2:
            st.metric("Max Loss", "₹4,200", "Limited")
        with col3:
            st.metric("Breakeven", f"₹{current_price + 12:.2f}", "+2.1%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Options chain
    st.markdown("### 📊 Live Options Chain")
    st.markdown('<div class="options-panel">', unsafe_allow_html=True)
    
    # Mock options chain data
    st.markdown('<div class="options-chain">', unsafe_allow_html=True)
    
    # Calls section
    st.markdown('<div class="call-options">', unsafe_allow_html=True)
    st.markdown("**📈 CALL OPTIONS**")
    call_strikes = [current_price - 40, current_price - 20, current_price, current_price + 20, current_price + 40]
    for strike in call_strikes:
        if strike >= current_price - 20:
            st.write(f"**₹{strike:.0f}** | OI: 1.5K | IV: 42% | LTP: ₹{premium + (strike - current_price)/50:.1f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Puts section
    st.markdown('<div class="put-options">', unsafe_allow_html=True)
    st.markdown("**📉 PUT OPTIONS**")
    for strike in call_strikes:
        if strike <= current_price + 20:
            st.write(f"**₹{strike:.0f}** | OI: 1.2K | IV: 45% | LTP: ₹{premium + (current_price - strike)/50:.1f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------- AI PREDICTIONS PAGE -----------------------
def show_ai_predictions():
    """Dedicated AI predictions page"""
    st.markdown(
        '<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; margin: 1rem 0;"><h2>🤖 AI-Powered Market Predictions</h2><p>Machine learning forecasts, sentiment analysis, and trading signals</p></div>',
        unsafe_allow_html=True,
    )
    
    # Current market context
    try:
        df = get_daily_data(ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
    except:
        current_price = 0
    
    # AI Models Overview
    st.markdown("### 🧠 AI Model Portfolio")
    
    models = [
        {"name": "LSTM Neural Network", "accuracy": "86%", "confidence": "High", "color": "#00ffcc"},
        {"name": "Random Forest Ensemble", "accuracy": "83%", "confidence": "Medium", "color": "#0099ff"},
        {"name": "Sentiment Analysis", "accuracy": "79%", "confidence": "Medium", "color": "#ffaa00"},
        {"name": "Technical Pattern Recognition", "accuracy": "81%", "confidence": "High", "color": "#ff00ff"}
    ]
    
    cols = st.columns(4)
    for i, (col, model) in enumerate(zip(cols, models)):
        with col:
            st.markdown(f"""
            <div class="ai-card">
                <div style="color: {model['color']}; font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 600; margin-bottom: 0.3rem;">{model['name']}</div>
                <div style="font-size: 0.9rem; color: #888;">Accuracy: {model['accuracy']}</div>
                <div style="font-size: 0.8rem; color: {model['color']};">{model['confidence']} Confidence</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Price Predictions
    st.markdown("### 📈 Price Forecasts")
    
    pred_cols = st.columns(4)
    timeframes = ["1 Day", "1 Week", "1 Month", "3 Months"]
    predictions = [current_price * 1.008, current_price * 1.025, current_price * 1.068, current_price * 1.152]
    changes = [0.8, 2.5, 6.8, 15.2]
    confidences = [85, 82, 78, 72]
    
    for i, (col, tf, pred, chg, conf) in enumerate(zip(pred_cols, timeframes, predictions, changes, confidences)):
        with col:
            st.metric(
                f"{tf} Forecast",
                f"₹{pred:.2f}",
                f"+{chg}%",
                delta_color="normal" if chg > 0 else "inverse"
            )
            st.progress(conf/100, text=f"Confidence: {conf}%")
    
    # Trading Signals
    st.markdown("### 🎯 AI Trading Signals")
    
    signal_cols = st.columns(4)
    with signal_cols[0]:
        st.markdown('<div class="prediction-badge">STRONG BUY</div>', unsafe_allow_html=True)
        st.metric("Primary Signal", "BUY", "92% Confidence")
    with signal_cols[1]:
        st.metric("Risk Level", "LOW", "Stable Trend")
    with signal_cols[2]:
        st.metric("Momentum", "ACCELERATING", "Rising")
    with signal_cols[3]:
        st.metric("Volatility", "MEDIUM", "Expected: 18%")
    
    # Sentiment Analysis
    st.markdown("### 😊 Market Sentiment Analysis")
    
    sentiment_cols = st.columns(3)
    with sentiment_cols[0]:
        st.metric("News Sentiment", "Bullish", "72% Positive")
    with sentiment_cols[1]:
        st.metric("Social Media", "Neutral", "55% Positive")
    with sentiment_cols[2]:
        st.metric("Analyst Ratings", "Very Bullish", "88% Buy")
    
    # Model Insights
    st.markdown("### 💡 Model Insights & Explanation")
    
    with st.expander("View AI Model Reasoning", expanded=True):
        st.write("""
        **LSTM Neural Network Analysis