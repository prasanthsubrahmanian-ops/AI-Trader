import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide")

# Sidebar Navigation - functional navigation!
section = st.sidebar.radio(
    "Go to", 
    ("Home", "Research Reports", "Options Trading", "Chart Analysis", "AI Predictions")
)

# Clean heading
st.markdown(
    '<h1 style="margin-top:1.4rem; font-size:2.2rem;font-weight:700; text-align:left;">PRASANTH AI Trading Insights</h1>',
    unsafe_allow_html=True
)

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
    st.write("Detailed AI-powered research reports will be displayed here. (Add your own reporting logic or files!)")

elif section == "Options Trading":
    st.subheader("Options Trading")
    st.write("Options trading analytics and tools appear here. (You can integrate options chain charts, strategies, etc.)")

elif section == "Chart Analysis":
    st.subheader("Chart Analysis")
    st.write("Comprehensive chart analysis and technical indicators displayed here. (Add more charting logic or uploads!)")

elif section == "AI Predictions":
    st.subheader("AI Predictions")
    st.write("Future AI-driven stock/option/market predictions would show here. (Plug in your models or upload prediction results!)")
