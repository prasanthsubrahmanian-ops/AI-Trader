import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide")

# Black theme for the whole app (main and sidebar)
st.markdown("""
    <style>
    body, .main, .block-container, .sidebar .sidebar-content {
        background-color: #111 !important;
        color: #fff !important;
    }
    .header-text {
        margin-top: 2rem;
        margin-bottom: 2rem;
        font-size: 2.2rem;
        font-weight: 700;
        color: #fff;
        text-align: left;
    }
    .landing-box {
        background-color: #222;
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin: 2rem 0;
        box-shadow: 0 2px 16px rgba(0,0,0,0.5);
    }
    h2, h3, h4 { color: #fff !important; }
    div[data-testid="stDataFrame"] { background-color: #222 !important; color: #fff !important;}
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation only (no user info)
section = st.sidebar.radio(
    "Navigation",
    ("Home", "Research Reports", "Options Trading", "Chart Analysis", "AI Predictions")
)

# Heading
st.markdown('<div class="header-text">PRASANTH AI Trading Insights</div>', unsafe_allow_html=True)

if section == "Home":
    stock_name = st.selectbox("Stock Name", ["TCS", "RELIANCE", "INFY", "NIFTY"])
    period = st.slider("Period (Days)", 10, 60, 30)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=period)
    base = np.linspace(1800, 2200, period) + np.random.normal(0, 20, period)
    df = pd.DataFrame({
        "Date": dates,
        "Open": base + np.random.normal(2, 2, period),
        "High": base + np.random.normal(10, 3, period),
        "Low": base - np.random.normal(10, 3, period),
        "Close": base + np.random.normal(0, 3, period),
        "Volume": np.random.randint(50000, 120000, period)
    })
    st.subheader(f"{stock_name} Price Chart")
    st.line_chart(df.set_index("Date")["Close"])
    st.subheader(f"{stock_name} OHLC Data")
    st.dataframe(df.set_index("Date")[["Open", "High", "Low", "Close"]])
    st.subheader(f"{stock_name} Trading Volume")
    st.bar_chart(df.set_index("Date")["Volume"])
    st.markdown("---")
    st.subheader("NIFTY Chart Example")
    nifty_days = 30
    nifty_dates = pd.date_range(end=pd.Timestamp.today(), periods=nifty_days)
    nifty = np.linspace(19500, 20000, nifty_days) + np.random.normal(0, 30, nifty_days)
    nifty_df = pd.DataFrame({"Date": nifty_dates, "NIFTY": nifty})
    st.line_chart(nifty_df.set_index("Date")["NIFTY"])

elif section == "Research Reports":
    st.markdown('<div class="landing-box"><h2>Research Reports</h2><p>Access detailed AI-powered market research here. (Customize this section to add your reports.)</p></div>', unsafe_allow_html=True)

elif section == "Options Trading":
    st.markdown('<div class="landing-box"><h2>Options Trading</h2><p>View analytics, strategies, and option chain visuals. (Expand this section for options tools.)</p></div>', unsafe_allow_html=True)

elif section == "Chart Analysis":
    st.markdown('<div class="landing-box"><h2>Chart Analysis</h2><p>Explore technical indicators and price charts here. (Customize this area for charting features.)</p></div>', unsafe_allow_html=True)

elif section == "AI Predictions":
    st.markdown('<div class="landing-box"><h2>AI Predictions</h2><p>Find AI-generated forecasts and signals. (Add model outputs or prediction charts here.)</p></div>', unsafe_allow_html=True)
