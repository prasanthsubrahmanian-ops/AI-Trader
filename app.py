import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide")

# Black background for all content
st.markdown("""
    <style>
        body, .main, .block-container {
            background-color: #111 !important;
            color: #fff !important;
        }
        .sidebar .sidebar-content, .css-1v0mbdj, .css-fblp2m {
            background-color: #111 !important;
            color: #fff !important;
        }
        .header-text {
            margin-top: 1.2rem;
            margin-bottom: 2rem;
            font-size: 2.2rem;
            font-weight: 700;
            color: #fff;
            text-align: left;
        }
        h2, h3, h4, h5 { color: #fff !important; }
        div[data-testid="stDataFrame"] { background-color: #222 !important; color: #fff !important;}
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation—no name/email at all
section = st.sidebar.radio(
    "Navigation",
    ("Home", "Research Reports", "Options Trading", "Chart Analysis", "AI Predictions")
)

# Main heading
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
    st.subheader("Research Reports")
    st.write("Detailed AI-powered research will be displayed here. Add your reports, visuals or upload content!")

elif section == "Options Trading":
    st.subheader("Options Trading")
    st.write("Options trading analytics and tools are displayed here. Integrate your options charts, signals, etc!")

elif section == "Chart Analysis":
    st.subheader("Chart Analysis")
    st.write("Technical chart analysis and indicators appear here. Expand with custom chart code or uploads.")

elif section == "AI Predictions":
    st.subheader("AI Predictions")
    st.write("AI-driven market predictions appear here. Plug in your models or show output data/results.")

