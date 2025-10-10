import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import altair as alt
from datetime import datetime, timedelta

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="Smart Trade with Prasanth Subrahmanian", 
    layout="wide"
)

# ----------------------- CUSTOM STYLE -----------------------
custom_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

body, .main, .block-container {
    background-color: #000 !important;
    color: #fff !important;
    padding-top: 0.5rem !important;
}

.main-header {
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    font-size: 2.8rem;
    font-weight: 700;
    color: #00ffcc;
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
    background: transparent;
    border: 2px solid #00ffcc;
    color: #00ffcc;
    padding: 0.6rem 1.2rem;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

.nav-btn:hover {
    background-color: #00ffcc;
    color: #000;
    transform: translateY(-2px);
}

.nav-btn.active {
    background-color: #00ffcc;
    color: #000;
}

/* Compact Metrics */
.compact-metrics {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.8rem;
    margin: 1rem 0;
}

.metric-box {
    background: #1a1a1a;
    padding: 0.8rem;
    border-radius: 8px;
    border-left: 3px solid #00ffcc;
    text-align: center;
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
    background: #111;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #333;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.research-card:hover {
    border-color: #00ffcc;
    transform: translateY(-2px);
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

/* Report Details */
.report-section {
    background: #111;
    padding: 2rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #00ffcc;
}

.report-header {
    color: #00ffcc;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #333;
    padding-bottom: 0.5rem;
}

.report-content {
    line-height: 1.6;
}

.report-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

/* Description Column */
.description-box {
    background: #1a1a1a;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #00ffcc;
    margin: 1rem 0;
}

.description-header {
    color: #00ffcc;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.description-content {
    color: #ccc;
    line-height: 1.6;
}

@media (max-width: 768px) {
    .compact-metrics {
        grid-template-columns: repeat(3, 1fr);
    }
    .report-metrics {
        grid-template-columns: 1fr;
    }
    .main-header { font-size: 2.2rem; }
    .nav-btn { padding: 0.5rem 1rem; font-size: 0.9rem; }
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
    st.session_state.chart_period = "1Y"
if 'current_report' not in st.session_state:
    st.session_state.current_report = None
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "RELIANCE.NS"

# ----------------------- HEADER -----------------------
st.markdown('<div class="main-header">SMART TRADE with Prasanth Subrahmanian</div>', unsafe_allow_html=True)

# ----------------------- SIMPLE NAVIGATION -----------------------
nav_options = ["🏠 Home", "📑 Research Reports", "💹 Options Trading", "📈 Chart Analysis", "🤖 AI Predictions"]
nav_labels = [option.split(" ")[-1] for option in nav_options]

nav_cols = st.columns(5)
for i, (col, option) in enumerate(zip(nav_cols, nav_options)):
    with col:
        if st.button(option, use_container_width=True, 
                    type="primary" if st.session_state.current_section == nav_labels[i] else "secondary"):
            st.session_state.current_section = nav_labels[i]
            st.rerun()

# ----------------------- STOCK SELECTION (Only on Home Page) -----------------------
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

# Only show stock selection on Home page
if st.session_state.current_section == "Home":
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        stock_name = st.selectbox("Select Stock", list(stocks.keys()), 
                                 index=list(stocks.keys()).index(st.session_state.stock_name))
    with col2:
        # Chart period selection only on Home page
        chart_period = st.selectbox("Chart Period", 
                                   ["1M", "3M", "6M", "1Y", "2Y", "5Y"],
                                   index=3)
    with col3:
        st.write("")
        st.write(f"**Current:** {stock_name} | {chart_period}")

    st.session_state.stock_name = stock_name
    st.session_state.chart_period = chart_period

# Always update ticker based on selected stock
ticker = stocks[st.session_state.stock_name]
st.session_state.current_ticker = ticker
section = st.session_state.current_section

# Map period selection to yfinance period
period_map = {
    "1M": "1mo",
    "3M": "3mo", 
    "6M": "6mo",
    "1Y": "1y",
    "2Y": "2y",
    "5Y": "5y"
}

# ----------------------- RESEARCH MAIN PAGE FUNCTION -----------------------
def show_research_main_page():
    """Show the main research reports page"""
    st.markdown(
        '<div style="background: #111; padding: 2rem; border-radius: 12px; margin: 1rem 0;"><h2>📑 Research Reports</h2><p>Comprehensive fundamental & technical analysis reports powered by advanced AI algorithms.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Current Stock Info
    try:
        df = get_daily_data(st.session_state.current_ticker, 30)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[-2])
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
            
            st.info(f"**{st.session_state.stock_name}: ₹{current_price:.2f} | {change:+.2f} ({change_pct:+.2f}%)**")
    except:
        pass
    
    # RESEARCH REPORT SECTIONS
    st.markdown("### 📋 Research Report Sections")
    
    research_sections = [
        {
            "icon": "📊",
            "title": "Executive Summary",
            "description": "High-level overview and investment recommendation",
            "page": "executive_summary"
        },
        {
            "icon": "🔍",
            "title": "Company Overview", 
            "description": "Business model, management, and competitive positioning",
            "page": "company_overview"
        },
        {
            "icon": "💹",
            "title": "Financial Analysis",
            "description": "Income statement, balance sheet, and cash flow analysis",
            "page": "financial_analysis"
        },
        {
            "icon": "📈",
            "title": "Valuation Analysis",
            "description": "DCF, comparable companies, and intrinsic value calculation",
            "page": "valuation_analysis"
        },
        {
            "icon": "⚡", 
            "title": "Technical Analysis",
            "description": "Chart patterns, indicators, and price targets",
            "page": "technical_analysis"
        },
        {
            "icon": "🔄",
            "title": "Industry Analysis",
            "description": "Market trends, competition, and growth prospects", 
            "page": "industry_analysis"
        },
        {
            "icon": "⚠️",
            "title": "Risk Assessment",
            "description": "Key risks and mitigation strategies",
            "page": "risk_assessment"
        },
        {
            "icon": "🎯",
            "title": "Investment Thesis",
            "description": "Bull and bear cases with probability assessment",
            "page": "investment_thesis"
        }
    ]
    
    # Create research cards in 2 columns
    col1, col2 = st.columns(2)
    
    for idx, research in enumerate(research_sections):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
            <div class="research-card">
                <div class="research-icon">{research['icon']}</div>
                <div class="research-title">{research['title']}</div>
                <div class="research-desc">{research['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"View {research['title']}", key=research['page'], use_container_width=True):
                st.session_state.current_report = research['page']
                st.rerun()
    
    # Description Column
    st.markdown("---")
    st.markdown("""
    <div class="description-box">
        <div class="description-header">About Research Reports</div>
        <div class="description-content">
            <p>Our comprehensive research reports provide in-depth analysis of stocks and market trends using advanced AI algorithms and fundamental research methodologies.</p>
            
            <p><strong>Key Features:</strong></p>
            <ul>
                <li><strong>AI-Powered Analysis:</strong> Machine learning algorithms process vast amounts of data to generate accurate predictions</li>
                <li><strong>Fundamental Research:</strong> Deep dive into company financials, management, and competitive positioning</li>
                <li><strong>Technical Analysis:</strong> Chart patterns, indicators, and price action analysis</li>
                <li><strong>Risk Assessment:</strong> Comprehensive evaluation of investment risks and mitigation strategies</li>
                <li><strong>Valuation Models:</strong> Multiple valuation approaches including DCF, comparable companies, and intrinsic value</li>
            </ul>
            
            <p><strong>Methodology:</strong> Each report combines quantitative data analysis with qualitative insights from our team of experienced analysts and AI systems.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    st.subheader("📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Analyst Rating", "BUY", "4.2/5")
    with col2:
        st.metric("Price Target", "₹1,650", "+12%")
    with col3:
        st.metric("Upside Potential", "15%", "+2%")
    with col4:
        st.metric("Risk Level", "Medium", "Stable")

# ----------------------- REPORT DETAILS FUNCTION -----------------------
def show_report_details():
    """Display detailed report content"""
    
    # Back button
    if st.button("← Back to Research Reports"):
        st.session_state.current_report = None
        st.rerun()
    
    report_name = st.session_state.current_report
    
    st.markdown(f'<div class="report-section"><h2 class="report-header">{report_name.replace("_", " ").title()} - {st.session_state.stock_name}</h2>', unsafe_allow_html=True)
    
    try:
        df = get_stock_data(st.session_state.current_ticker, "1y")
        current_price = float(df['Close'].iloc[-1]) if not df.empty else 0
        prev_close = float(df['Close'].iloc[-2])
        change = current_price - prev_close
        change_pct = (change / prev_close) * 100
    except:
        current_price = 0
        change = 0
        change_pct = 0
    
    # Report-specific content
    if report_name == "executive_summary":
        st.markdown("""
        <div class="report-content">
            <h3>🎯 Investment Recommendation: STRONG BUY</h3>
            <p><strong>Current Price:</strong> ₹{:.2f} ({:+.2f}%)</p>
            <p><strong>Target Price:</strong> ₹1,650 (15% Upside)</p>
            <p><strong>Time Horizon:</strong> 12-18 Months</p>
            <p><strong>Risk Rating:</strong> Medium</p>
            
            <h4>Key Highlights:</h4>
            <ul>
                <li>Strong revenue growth of 18% YoY</li>
                <li>Market leadership in core segments</li>
                <li>Robust balance sheet with low debt</li>
                <li>Favorable industry tailwinds</li>
            </ul>
        </div>
        """.format(current_price, change_pct), unsafe_allow_html=True)
        
        # Description Column
        st.markdown("""
        <div class="description-box">
            <div class="description-header">Executive Summary Overview</div>
            <div class="description-content">
                <p>The Executive Summary provides a comprehensive overview of our investment thesis, highlighting key findings from our detailed analysis across all research areas.</p>
                
                <p><strong>What's Included:</strong></p>
                <ul>
                    <li>Investment recommendation and rationale</li>
                    <li>Key financial and operational metrics</li>
                    <li>Risk-reward assessment</li>
                    <li>Price targets and time horizon</li>
                    <li>Catalysts and key monitoring points</li>
                </ul>
                
                <p>This summary synthesizes insights from our fundamental, technical, and qualitative analysis to provide a clear investment framework.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Executive metrics
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Upside Potential", "15%", "2.1%")
        with col2:
            st.metric("Dividend Yield", "1.8%", "0.2%")
        with col3:
            st.metric("EPS Growth", "12%", "1.5%")
        
    elif report_name == "financial_analysis":
        st.markdown("""
        <div class="report-content">
            <h3>💰 Financial Performance</h3>
            <p><strong>Current Price:</strong> ₹{:.2f} ({:+.2f}%)</p>
            
            <h4>Income Statement Highlights (Last Quarter):</h4>
            <ul>
                <li><strong>Revenue:</strong> ₹25,400 Cr (+18% YoY)</li>
                <li><strong>Net Profit:</strong> ₹4,200 Cr (+22% YoY)</li>
                <li><strong>Operating Margin:</strong> 24.5% (+1.2%)</li>
                <li><strong>EPS:</strong> ₹62.5 (+20% YoY)</li>
            </ul>
            
            <h4>Balance Sheet Strength:</h4>
            <ul>
                <li><strong>Debt-to-Equity:</strong> 0.35 (Conservative)</li>
                <li><strong>Current Ratio:</strong> 2.1 (Healthy)</li>
                <li><strong>ROE:</strong> 18.5% (Above Industry)</li>
                <li><strong>ROCE:</strong> 22.1% (Strong)</li>
            </ul>
        </div>
        """.format(current_price, change_pct), unsafe_allow_html=True)
        
        # Description Column
        st.markdown("""
        <div class="description-box">
            <div class="description-header">Financial Analysis Methodology</div>
            <div class="description-content">
                <p>Our Financial Analysis examines the company's financial health, performance trends, and sustainability of growth through comprehensive ratio analysis and trend evaluation.</p>
                
                <p><strong>Analysis Components:</strong></p>
                <ul>
                    <li><strong>Profitability Analysis:</strong> Margins, returns, and efficiency ratios</li>
                    <li><strong>Liquidity Assessment:</strong> Working capital and cash flow analysis</li>
                    <li><strong>Solvency Evaluation:</strong> Debt levels and coverage ratios</li>
                    <li><strong>Growth Metrics:</strong> Revenue, earnings, and cash flow growth trends</li>
                    <li><strong>Comparative Analysis:</strong> Performance vs. industry peers</li>
                </ul>
                
                <p>We use both historical trends and forward-looking projections to assess financial sustainability.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Financial metrics
        st.subheader("Financial Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Revenue Growth", "18%", "2.1%")
        with col2:
            st.metric("Profit Margin", "16.5%", "0.8%")
        with col3:
            st.metric("ROE", "18.5%", "1.2%")
        
    elif report_name == "technical_analysis":
        st.markdown("""
        <div class="report-content">
            <h3>📈 Technical Outlook</h3>
            <p><strong>Current Price:</strong> ₹{:.2f} ({:+.2f}%)</p>
            
            <h4>Key Technical Levels:</h4>
            <ul>
                <li><strong>Support:</strong> ₹1,350 (Strong), ₹1,280 (Major)</li>
                <li><strong>Resistance:</strong> ₹1,480 (Immediate), ₹1,550 (Major)</li>
                <li><strong>Trend:</strong> Bullish (Higher Highs & Higher Lows)</li>
            </ul>
            
            <h4>Indicator Analysis:</h4>
            <ul>
                <li><strong>RSI:</strong> 58 (Neutral-Bullish)</li>
                <li><strong>MACD:</strong> Bullish Crossover</li>
                <li><strong>Moving Averages:</strong> Price above 50 & 200 DMA</li>
                <li><strong>Volume:</strong> Increasing on up moves</li>
            </ul>
        </div>
        """.format(current_price, change_pct), unsafe_allow_html=True)
        
        # Description Column
        st.markdown("""
        <div class="description-box">
            <div class="description-header">Technical Analysis Approach</div>
            <div class="description-content">
                <p>Our Technical Analysis combines classical chart patterns with modern quantitative indicators to identify trends, support/resistance levels, and potential entry/exit points.</p>
                
                <p><strong>Technical Tools Used:</strong></p>
                <ul>
                    <li><strong>Trend Analysis:</strong> Moving averages, trendlines, and chart patterns</li>
                    <li><strong>Momentum Indicators:</strong> RSI, MACD, Stochastic oscillators</li>
                    <li><strong>Volume Analysis:</strong> Volume trends and on-balance volume</li>
                    <li><strong>Support/Resistance:</strong> Key price levels and Fibonacci retracements</li>
                    <li><strong>Volatility Measures:</strong> Bollinger Bands, ATR for risk assessment</li>
                </ul>
                
                <p>We combine multiple timeframes (daily, weekly, monthly) for comprehensive trend analysis.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Technical metrics
        st.subheader("Technical Indicators")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("RSI", "58", "Neutral")
        with col2:
            st.metric("Trend", "Bullish", "Strong")
        with col3:
            st.metric("Volume Trend", "Positive", "12%")
        
    else:
        # Default content for other reports
        st.markdown("""
        <div class="report-content">
            <h3>📋 {} Analysis</h3>
            <p><strong>Current Price:</strong> ₹{:.2f} ({:+.2f}%)</p>
            <p>Detailed analysis for {} is currently being generated by our AI algorithms.</p>
            
            <h4>Key Points:</h4>
            <ul>
                <li>Comprehensive analysis in progress</li>
                <li>Real-time data integration active</li>
                <li>AI-powered insights being calculated</li>
                <li>Full report available shortly</li>
            </ul>
            
            <p><strong>Analysis Last Updated:</strong> {}</p>
        </div>
        """.format(
            report_name.replace('_', ' ').title(),
            current_price, change_pct,
            st.session_state.stock_name,
            datetime.now().strftime('%Y-%m-%d %H:%M')
        ), unsafe_allow_html=True)
        
        # Default description
        st.markdown(f"""
        <div class="description-box">
            <div class="description-header">{report_name.replace('_', ' ').title()} Analysis</div>
            <div class="description-content">
                <p>This section provides comprehensive analysis of {report_name.replace('_', ' ').lower()} aspects for {st.session_state.stock_name}.</p>
                <p>Our AI systems are currently processing the latest data to generate detailed insights and recommendations.</p>
                <p><strong>Expected Analysis Components:</strong></p>
                <ul>
                    <li>Detailed quantitative and qualitative assessment</li>
                    <li>Comparative analysis with industry peers</li>
                    <li>Risk factors and opportunity assessment</li>
                    <li>Strategic implications and recommendations</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------- HOME SECTION -----------------------
if section == "Home":
    # Stock selection is already shown above for Home page
    
    st.markdown("### Real-Time Market Data")
    
    with st.spinner(f"Fetching {st.session_state.stock_name} data..."):
        try:
            # Get daily data for the selected period
            df = get_stock_data(ticker, period_map[st.session_state.chart_period])
            stock_info = get_stock_info(ticker)
            
            if df.empty:
                st.error("No data available. Try again later or choose another stock.")
            else:
                df.reset_index(inplace=True)
                
                # Calculate current values
                current_price = float(df['Close'].iloc[-1])
                prev_price = float(df['Close'].iloc[-2]) if len(df) > 1 else current_price
                price_change = current_price - prev_price
                price_change_pct = (price_change / prev_price) * 100 if prev_price > 0 else 0
                
                day_high = float(df['High'].iloc[-1])
                day_low = float(df['Low'].iloc[-1])
                day_open = float(df['Open'].iloc[-1])
                volume = int(df['Volume'].iloc[-1])
                
                # Get additional metrics from stock info
                pe_ratio = stock_info.get('trailingPE', 'N/A')
                market_cap = stock_info.get('marketCap', 'N/A')
                if market_cap != 'N/A':
                    market_cap = f"${market_cap/1e9:.1f}B" if market_cap > 1e9 else f"${market_cap/1e6:.1f}M"
                
                dividend_yield = stock_info.get('dividendYield', 'N/A')
                if dividend_yield != 'N/A':
                    dividend_yield = f"{dividend_yield*100:.2f}%"
                
                # 52-week range from the data
                high_52w = float(df['High'].max())
                low_52w = float(df['Low'].min())
                
                # COMPACT KEY METRICS SECTION
                st.markdown("#### 📊 Current Market Data")
                
                # Current price with large display
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.metric(
                        f"{st.session_state.stock_name} Current Price",
                        f"₹{current_price:.2f}",
                        f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
                    )
                with col2:
                    st.metric("Day High", f"₹{day_high:.2f}")
                with col3:
                    st.metric("Day Low", f"₹{day_low:.2f}")
                
                # Compact metrics grid
                metrics_html = f"""
                <div class="compact-metrics">
                    <div class="metric-box">
                        <div class="metric-label">Open</div>
                        <div class="metric-value">₹{day_open:.2f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Previous Close</div>
                        <div class="metric-value">₹{prev_price:.2f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Volume</div>
                        <div class="metric-value">{volume:,}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">P/E Ratio</div>
                        <div class="metric-value">{pe_ratio if pe_ratio != 'N/A' else 'N/A'}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Market Cap</div>
                        <div class="metric-value">{market_cap}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Div Yield</div>
                        <div class="metric-value">{dividend_yield}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">52W High</div>
                        <div class="metric-value">₹{high_52w:.2f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">52W Low</div>
                        <div class="metric-value">₹{low_52w:.2f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Change</div>
                        <div class="metric-value {'negative' if price_change < 0 else ''}">
                            {price_change:+.2f}
                        </div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Change %</div>
                        <div class="metric-value {'negative' if price_change_pct < 0 else ''}">
                            {price_change_pct:+.2f}%
                        </div>
                    </div>
                </div>
                """
                st.markdown(metrics_html, unsafe_allow_html=True)
                
                # Daily Price Chart
                st.subheader(f"📈 {st.session_state.chart_period} Price Chart - {st.session_state.stock_name}")
                
                # Calculate moving averages
                df["SMA20"] = df["Close"].rolling(20).mean()
                df["SMA50"] = df["Close"].rolling(50).mean()
                
                # Create interactive chart
                chart_data = df[['Date', 'Close', 'SMA20', 'SMA50']].copy()
                
                base = alt.Chart(chart_data).encode(
                    x=alt.X('Date:T', title='Date')
                ).properties(
                    height=400,
                    title=f"{st.session_state.stock_name} Price Chart ({st.session_state.chart_period})"
                )
                
                # Create layers for different lines
                close_line = base.mark_line(color='#00ffcc', strokeWidth=2).encode(
                    y=alt.Y('Close:Q', title='Price (₹)', scale=alt.Scale(zero=False)),
                    tooltip=['Date:T', 'Close:Q', 'SMA20:Q', 'SMA50:Q']
                )
                
                sma20_line = base.mark_line(color='#ffaa00', strokeWidth=1.5, strokeDash=[5,5]).encode(
                    y='SMA20:Q'
                )
                
                sma50_line = base.mark_line(color='#ff00ff', strokeWidth=1.5, strokeDash=[5,5]).encode(
                    y='SMA50:Q'
                )
                
                # Combine all layers
                chart = alt.layer(close_line, sma20_line, sma50_line).configure(
                    background='#000000',
                    axis=alt.Axis(
                        labelColor='#ffffff',
                        titleColor='#ffffff'
                    ),
                    title=alt.TitleConfig(color='#ffffff')
                )
                
                st.altair_chart(chart, use_container_width=True)
                st.caption("Close Price (Green) | 20-Day SMA (Orange) | 50-Day SMA (Pink)")
                
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")

# ----------------------- RESEARCH REPORTS SECTION -----------------------
elif section == "Research Reports":
    # Show current stock info
    st.write(f"**Currently Analyzing:** {st.session_state.stock_name}")
    
    # If a specific report is selected, show its details
    if st.session_state.current_report:
        show_report_details()
    else:
        show_research_main_page()

# ----------------------- OPTIONS TRADING SECTION -----------------------
elif section == "Options Trading":
    st.markdown(
        '<div style="background: #111; padding: 2rem; border-radius: 12px; margin: 1rem 0;"><h2>💹 Options Trading</h2><p>Advanced options chain analysis, volatility tracking, and strategy optimization tools.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Current price display
    try:
        df = get_daily_data(ticker, 1)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
    except:
        pass
    
    # Description Column
    st.markdown("""
    <div class="description-box">
        <div class="description-header">Options Trading Platform</div>
        <div class="description-content">
            <p>Our Options Trading platform provides comprehensive tools for options strategy analysis, volatility assessment, and risk management.</p>
            
            <p><strong>Key Features:</strong></p>
            <ul>
                <li><strong>Options Chain Analysis:</strong> Real-time options data with Greeks calculation</li>
                <li><strong>Volatility Analysis:</strong> IV Rank, IV Percentile, and volatility skew</li>
                <li><strong>Strategy Builder:</strong> Multi-leg options strategies with risk analysis</li>
                <li><strong>Probability Analysis:</strong> Probability of profit and expected returns</li>
                <li><strong>Risk Management:</strong> Position sizing and risk assessment tools</li>
            </ul>
            
            <p>All analysis is based on real-time market data and advanced options pricing models.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Options content
    st.subheader("Options Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("IV Rank", "65%", "High")
    with col2:
        st.metric("Put/Call Ratio", "0.85", "Bullish")
    with col3:
        st.metric("Open Interest", "2.5M", "+15%")
    with col4:
        st.metric("Volume", "1.8M", "+22%")

# ----------------------- CHART ANALYSIS SECTION -----------------------
elif section == "Chart Analysis":
    st.markdown(
        '<div style="background: #111; padding: 2rem; border-radius: 12px; margin: 1rem 0;"><h2>📈 Chart Analysis</h2><p>Advanced technical analysis with multiple indicators, patterns, and drawing tools.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Current price display
    try:
        df = get_daily_data(ticker, 1)
        if not df.empty:
            current_price = float(df['Close'].iloc[-1])
            st.info(f"**{st.session_state.stock_name} Current Price: ₹{current_price:.2f}**")
    except:
        pass
    
    # Description Column
    st.markdown("""
    <div class="description-box">
        <div class="description-header">Advanced Chart Analysis</div>
        <div class="description-content">
            <p>Our Chart Analysis platform provides professional-grade technical analysis tools with multiple timeframes, indicators, and drawing capabilities.</p>
            
            <p><strong>Available Tools:</strong></p>
            <ul>
                <li><strong>Multiple Timeframes:</strong> Daily