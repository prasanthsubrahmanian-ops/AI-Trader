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

.stock-selector {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin: 1rem 0;
    align-items: center;
    flex-wrap: wrap;
}

.landing-box {
    background-color: #111;
    padding: 2rem 2.5rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    box-shadow: 0 4px 24px rgba(255, 255, 255, 0.1);
}

.section-header {
    color: #00ffcc !important;
    margin-top: 0.2rem !important;
    margin-bottom: 1rem !important;
}

h2, h3, h4, p, label {
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

@media (max-width: 768px) {
    .compact-metrics {
        grid-template-columns: repeat(3, 1fr);
    }
    .research-grid {
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
    st.markdown("### Research Report Sections")
    
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
    
    st.markdown('<div class="research-grid">', unsafe_allow_html=True)
    
    for section in research_sections:
        st.markdown(f"""
        <div class="research-card" onclick="navigateTo('{section['page']}')">
            <div class="research-icon">{section['icon']}</div>
            <div class="research-title">{section['title']}</div>
            <div class="research-desc">{section['description']}</div>
            <button class="research-btn" onclick="event.stopPropagation(); navigateTo('{section['page']}')">
                View Report →
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # JavaScript for navigation
    st.markdown("""
    <script>
    function navigateTo(page) {
        // In a real app, this would navigate to different pages
        // For demo, we'll show an alert
        alert('Navigating to: ' + page + ' report page\\n\\nIn a full implementation, this would open a separate page with detailed analysis.');
        
        // For Streamlit multi-page app, you could use:
        // window.location.href = page + '.py';
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    st.subheader("Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Analyst Rating", "BUY", "4.2/5")
    with col2:
        st.metric("Price Target", "₹1,650", "+12%")
    with col3:
        st.metric("Upside Potential", "15%", "+2%")
    with col4:
        st.metric("Risk Level", "Medium", "Stable")

# ----------------------- OTHER SECTIONS (Options, Chart, AI) -----------------------
elif section == "Options Trading":
    st.markdown(
        '<div class="landing-box"><h2>💹 Options Trading</h2><p>Advanced options chain analysis, volatility tracking, and strategy optimization tools.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Compact metrics for options
    st.markdown("#### Options Key Metrics")
    st.markdown("""
    <div class="compact-metrics">
        <div class="metric-box">
            <div class="metric-label">IV Rank</div>
            <div class="metric-value">65%</div>
            <div class="metric-change">High</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Put/Call Ratio</div>
            <div class="metric-value">0.85</div>
            <div class="metric-change">Bullish</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Open Interest</div>
            <div class="metric-value">2.5M</div>
            <div class="metric-change">+15%</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Volume</div>
            <div class="metric-value">1.8M</div>
            <div class="metric-change">+22%</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">VIX</div>
            <div class="metric-value">18.2</div>
            <div class="metric-change negative">-0.5</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif section == "Chart Analysis":
    st.markdown(
        '<div class="landing-box"><h2>📈 Chart Analysis</h2><p>Advanced technical analysis with multiple indicators, patterns, and drawing tools.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Compact metrics for technical analysis
    st.markdown("#### Technical Indicators")
    st.markdown("""
    <div class="compact-metrics">
        <div class="metric-box">
            <div class="metric-label">RSI</div>
            <div class="metric-value">54.2</div>
            <div class="metric-change">Neutral</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">MACD</div>
            <div class="metric-value">Bullish</div>
            <div class="metric-change">↑</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Support</div>
            <div class="metric-value">₹1,350</div>
            <div class="metric-change">Strong</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Resistance</div>
            <div class="metric-value">₹1,480</div>
            <div class="metric-change">Moderate</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Trend</div>
            <div class="metric-value">Uptrend</div>
            <div class="metric-change">Strong</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif section == "AI Predictions":
    st.markdown(
        '<div class="landing-box"><h2>🤖 AI Predictions</h2><p>Machine learning powered price predictions, sentiment analysis, and trading signals.</p></div>',
        unsafe_allow_html=True,
    )
    
    # Compact metrics for AI predictions
    st.markdown("#### AI Analysis Metrics")
    st.markdown("""
    <div class="compact-metrics">
        <div class="metric-box">
            <div class="metric-label">AI Signal</div>
            <div class="metric-value">BUY</div>
            <div class="metric-change">Strong</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Confidence</div>
            <div class="metric-value">85%</div>
            <div class="metric-change">High</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">1W Target</div>
            <div class="metric-value">₹1,420</div>
            <div class="metric-change">+3.1%</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">1M Target</div>
            <div class="metric-value">₹1,520</div>
            <div class="metric-change">+10.4%</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Stop Loss</div>
            <div class="metric-value">₹1,320</div>
            <div class="metric-change negative">-4.2%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>SMART TRADE with Prasanth Subrahmanian • Real-time Market Data</div>", unsafe_allow_html=True)