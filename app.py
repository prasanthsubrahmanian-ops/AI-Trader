import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide", initial_sidebar_state="expanded")

# SIDEBAR - only inputs, no navigation letters
st.sidebar.markdown("### Stock Selection")
stock_name = st.sidebar.selectbox("Stock Name", ["TCS", "RELIANCE", "INFY", "NIFTY"])
period = st.sidebar.slider("Period (Days)", 10, 60, 30)
show_chart = st.sidebar.button("Show Price Chart")
st.sidebar.caption("Built with Streamlit | pandas | NumPy")

# SIMPLE HEADER (no blue color background, no icon)
st.markdown("""
    <div style="padding: 18px 0 18px 0; border-bottom: 1px solid #ddd; margin-bottom: 24px;">
        <h1 style="text-align:center; margin:0; font-weight: 700; font-size: 2.5rem; color: #222;">
            PRASANTH AI Trading Insights
        </h1>
    </div>
""", unsafe_allow_html=True)

if show_chart:
    st.subheader(f"{stock_name} Price Chart & OHLC (Last {period} Days)")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=period)
    base = np.linspace(1800, 2200, period) + np.random.normal(0, 20, period)
    df = pd.DataFrame({
        'Date': dates,
        'Open': base + np.random.normal(2, 2, period),
        'High': base + np.random.normal(10, 3, period),
        'Low': base - np.random.normal(10, 3, period),
        'Close': base + np.random.normal(0, 3, period)
    })
    st.line_chart(df.set_index("Date")["Close"])
    st.dataframe(df.set_index("Date")[["Open", "High", "Low", "Close"]])

st.markdown("---")
st.subheader("NIFTY Chart Example")
nifty_days = 30
nifty_dates = pd.date_range(end=pd.Timestamp.today(), periods=nifty_days)
nifty = np.linspace(19500, 20000, nifty_days) + np.random.normal(0, 25, nifty_days)
nifty_df = pd.DataFrame({"Date": nifty_dates, "NIFTY": nifty})
st.line_chart(nifty_df.set_index("Date")["NIFTY"])

# Remove excess dark theme styling for simpler look (optional)
