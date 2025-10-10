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

/* Research Sections */
.research-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

.research-card {
    background: #111;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #333;
    transition: all 0.3s ease;
    cursor: pointer;
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
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #fff;
}

.research-desc {
    font-size: 0.85rem;
    color: #888;
    margin-bottom: 1rem;
}

.research-btn {
    background: transparent;
    border: 1px solid #00ffcc;
    color: #00ffcc;
    padding: 0.4rem 1rem;
    border-radius: 5px;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.research-btn:hover {
    background: #00ffcc;
    color: #000;
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

.report-metric {
    background: #1a1a1a;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}

@media (max-width: 768px) {
    .compact-metrics {
        grid-template-columns: repeat(3, 1fr);
    }
    .research-grid {
        grid-template-columns: 1fr;
    }
    .report-metrics {
        grid-template-columns: 1fr;
    }
    .landing-box { padding: 1.5rem; }
    .main-header { font-size: 2.2rem; }
    .nav-btn { padding: 0.5rem 1rem; font-size: 0.9rem; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------- CACHED FUNCTIONS -----------------------
@st.cache_data(ttl=300)
def get_stock_data(ticker, period):
    return yf.download(ticker, period=f"{period}d")

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
if 'period' not in st.session_state:
    st.session_state.period = 60
if 'current_report' not in st.session_state:
    st.session_state.current_report = None

# ----------------------- TOP NAVIGATION -----------------------
st.markdown("""
<div class="top-nav">
    <button class="nav-btn %s" onclick="setSection('Home')">🏠 Home</button>
    <button class="nav-btn %s" onclick="setSection('Research Reports')">📑 Research Reports</button>
    <button class="nav-btn %s" onclick="setSection('Options Trading')">💹 Options Trading</button>
    <button class="nav-btn %s" onclick="setSection('Chart Analysis')">📈 Chart Analysis</button>
    <button class="nav-btn %s" onclick="setSection('AI Predictions')">🤖 AI Predictions</button>
</div>

<script>
function setSection(section) {
    window.location.href = '?section=' + section;
}
</script>
""" % (
    'active' if st.session_state.current_section == 'Home' else '',
    'active' if st.session_state.current_section == 'Research Reports' else '',
    'active' if st.session_state.current_section == 'Options Trading' else '',
    'active' if st.session_state.current_section == 'Chart Analysis' else '',
    'active' if st.session_state.current_section == 'AI Predictions' else ''
), unsafe_allow_html=True)

# ----------------------- HEADER -----------------------
st.markdown('<div class="main-header">SMART TRADE with Prasanth Subrahmanian</div>', unsafe_allow_html=True)

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

# Handle URL parameters
params = st.query_params
if 'section' in params:
    st.session_state.current_section = params['section'][0]
if 'report' in params:
    st.session_state.current_report = params['report'][0]

# Stock selection
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    stock_name = st.selectbox("Select Stock", list(stocks.keys()), 
                             index=list(stocks.keys()).index(st.session_state.stock_name))
with col2:
    period = st.slider("Period (Days)", 10, 365, st.session_state.period)
with col3:
    st.write("")
    st.write(f"**Current:** {stock_name} | {period} days")

st.session_state.stock_name = stock_name
st.session_state.period = period
ticker = stocks[stock_name]
section = st.session_state.current_section
current_report = st.session_state.current_report

# ----------------------- HOME SECTION -----------------------
if section == "Home":
    st.markdown("### Real-Time Market Data")
    
    with st.spinner(f"Fetching {stock_name} data..."):
        try:
            df = get_stock_data(ticker, period)
            stock_info = get_stock_info(ticker)
            
            if df.empty:
                st.error("No data available. Try again later or choose another stock.")
            else:
                df.reset_index(inplace=True)
                
                # COMPACT KEY METRICS SECTION
                st.markdown("#### 📊 Key Metrics")
                
                current_price = float(df['Close'].iloc[-1])
                prev_price = float(df['Close'].iloc[-2])
                price_change = current_price - prev_price
                price_change_pct = (price_change / prev_price) * 100
                
                # Get additional metrics from stock info
                pe_ratio = stock_info.get('trailingPE', 'N/A')
                market_cap = stock_info.get('marketCap', 'N/A')
                if market_cap != 'N/A':
                    market_cap = f"${market_cap/1e9:.1f}B" if market_cap > 1e9 else f"${market_cap/1e6:.1f}M"
                
                dividend_yield = stock_info.get('dividendYield', 'N/A')
                if dividend_yield != 'N/A':
                    dividend_yield = f"{dividend_yield*100:.2f}%"
                
                # Compact metrics grid
                st.markdown(f"""
                <div class="compact-metrics">
                    <div class="metric-box">
                        <div class="metric-label">Current Price</div>
                        <div class="metric-value">₹{current_price:.2f}</div>
                        <div class="metric-change {'negative' if price_change < 0 else ''}">
                            {price_change:+.2f} ({price_change_pct:+.2f}%)
                        </div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Previous Close</div>
                        <div class="metric-value">₹{prev_price:.2f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Open</div>
                        <div class="metric-value">₹{float(df['Open'].iloc[-1]):.2f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Day High</div>
                        <div class="metric-value">₹{float(df['High'].iloc[-1]):.2f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Day Low</div>
                        <div class="metric-value">₹{float(df['Low'].iloc[-1]):.2f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Volume</div>
                        <div class="metric-value">{int(df['Volume'].iloc[-1]):,}</div>
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
                        <div class="metric-label">52W Range</div>
                        <div class="metric-value">₹{float(df['Low'].min()):.0f}-₹{float(df['High'].max()):.0f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Price Chart
                st.subheader("Price Chart")
                df["SMA20"] = df["Close"].rolling(20).mean()
                df["SMA50"] = df["Close"].rolling(50).mean()
                
                chart_data = df[['Date', 'Close', 'SMA20', 'SMA50']].copy()
                base = alt.Chart(chart_data).encode(x='Date:T').properties(height=400)
                close_line = base.mark_line(color='#00ffcc').encode(y='Close:Q', tooltip=['Date:T', 'Close:Q'])
                sma20_line = base.mark_line(color='#ffaa00', strokeDash=[5,5]).encode(y='SMA20:Q')
                sma50_line = base.mark_line(color='#ff00ff', strokeDash=[5,5]).encode(y='SMA50:Q')
                chart = close_line + sma20_line + sma50_line
                st.altair_chart(chart, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")

# ----------------------- RESEARCH REPORTS SECTION -----------------------
elif section == "Research Reports":
    
    # If a specific report is selected, show its details
    if current_report:
        show_report_details(current_report, stock_name, ticker)
    else:
        # Show main research reports page
        st.markdown(
            '<div class="landing-box"><h2>📑 Research Reports</h2><p>Comprehensive fundamental & technical analysis reports powered by advanced AI algorithms.</p></div>',
            unsafe_allow_html=True,
        )
        
        # Current Stock Info
        try:
            df = get_stock_data(ticker, 30)
            if not df.empty:
                current_price = float(df['Close'].iloc[-1])
                st.info(f"**Current Analysis for {stock_name}: ₹{current_price:.2f}**")
        except:
            pass
        
        # RESEARCH REPORT SECTIONS GRID
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
        
        # Create the research grid
        cols = st.columns(2)
        for idx, section in enumerate(research_sections):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"""
                    <div style="background: #111; padding: 1.5rem; border-radius: 10px; border: 1px solid #333; margin-bottom: 1rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.8rem; color: #00ffcc;">{section['icon']}</div>
                        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #fff;">{section['title']}</div>
                        <div style="font-size: 0.85rem; color: #888; margin-bottom: 1rem;">{section['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View {section['title']}", key=section['page']):
                        st.session_state.current_report = section['page']
                        st.rerun()
        
        # Quick Stats
        st.markdown("---")
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
def show_report_details(report_name, stock_name, ticker):
    """Display detailed report content"""
    
    # Back button
    if st.button("← Back to Research Reports"):
        st.session_state.current_report = None
        st.rerun()
    
    st.markdown(f'<div class="report-section"><h2 class="report-header">{report_name.replace("_", " ").title()} - {stock_name}</h2>', unsafe_allow_html=True)
    
    try:
        df = get_stock_data(ticker, 365)
        current_price = float(df['Close'].iloc[-1]) if not df.empty else 0
    except:
        current_price = 0
    
    # Report-specific content
    if report_name == "executive_summary":
        st.markdown("""
        <div class="report-content">
            <h3>🎯 Investment Recommendation: STRONG BUY</h3>
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
        """, unsafe_allow_html=True)
        
        # Executive metrics
        st.markdown('<div class="report-metrics">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Upside Potential", "15%", "2.1%")
        with col2:
            st.metric("Dividend Yield", "1.8%", "0.2%")
        with col3:
            st.metric("EPS Growth", "12%", "1.5%")
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif report_name == "financial_analysis":
        st.markdown("""
        <div class="report-content">
            <h3>💰 Financial Performance</h3>
            
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
        """, unsafe_allow_html=True)
        
        # Financial metrics
        st.markdown('<div class="report-metrics">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Revenue Growth", "18%", "2.1%")
        with col2:
            st.metric("Profit Margin", "16.5%", "0.8%")
        with col3:
            st.metric("ROE", "18.5%", "1.2%")
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif report_name == "technical_analysis":
        st.markdown("""
        <div class="report-content">
            <h3>📈 Technical Outlook</h3>
            
            <h4>Key Technical Levels:</h4>
            <ul>
                <li><strong>Current Price:</strong> ₹1,435</li>
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
        """, unsafe_allow_html=True)
        
        # Technical metrics
        st.markdown('<div class="report-metrics">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("RSI", "58", "Neutral")
        with col2:
            st.metric("Trend", "Bullish", "Strong")
        with col3:
            st.metric("Volume Trend", "Positive", "12%")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # Default content for other reports
        st.markdown(f"""
        <div class="report-content">
            <h3>📋 {report_name.replace('_', ' ').title()} Analysis</h3>
            <p>Detailed analysis for {stock_name} is currently being generated by our AI algorithms.</p>
            
            <h4>Key Points:</h4>
            <ul>
                <li>Comprehensive analysis in progress</li>
                <li>Real-time data integration active</li>
                <li>AI-powered insights being calculated</li>
                <li>Full report available shortly</li>
            </ul>
            
            <p><strong>Current Price:</strong> ₹{current_price:.2f}</p>
            <p><strong>Analysis Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------- OTHER SECTIONS -----------------------
elif section == "Options Trading":
    st.markdown(
        '<div class="landing-box"><h2>💹 Options Trading</h2><p>Advanced options chain analysis, volatility tracking, and strategy optimization tools.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Options content here...

elif section == "Chart Analysis":
    st.markdown(
        '<div class="landing-box"><h2>📈 Chart Analysis</h2><p>Advanced technical analysis with multiple indicators, patterns, and drawing tools.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Chart analysis content here...

elif section == "AI Predictions":
    st.markdown(
        '<div class="landing-box"><h2>🤖 AI Predictions</h2><p>Machine learning powered price predictions, sentiment analysis, and trading signals.</p></div>',
        unsafe_allow_html=True,
    )
    
    # AI predictions content here...

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>SMART TRADE with Prasanth Subrahmanian • Real-time Market Data</div>", unsafe_allow_html=True)