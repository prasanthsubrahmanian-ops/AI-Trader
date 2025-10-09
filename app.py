import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide", initial_sidebar_state="expanded")

# SIDEBAR
st.sidebar.markdown("## 📂 Navigation")
section = st.sidebar.radio(
    "Go to",
    ["Home", "Research Reports", "Option Trading AI", "Chart Analysis"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("### Stock Selection")
stock_name = st.sidebar.selectbox("Stock Name", ["TCS", "RELIANCE", "INFY", "NIFTY"])
period = st.sidebar.slider("Period (Days)", 10, 60, 30)
show_chart = st.sidebar.button("Show Price Chart")
st.sidebar.caption("Built with Streamlit | pandas | NumPy")

if section == "Home":
    st.markdown("""
        <div style="background-color:#1565c0;padding:28px 0 18px 0; border-radius:16px;margin-bottom:24px;">
            <h1 style="color:white;text-align:center; margin:0;">
                <span style="font-size:2.0rem;vertical-align:middle;">📈</span>
                <span style="vertical-align:middle;font-size:2.4rem;">PRASANTH AI Trading Insights</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)

    # Stock chart and OHLC display only when button is pressed
    if show_chart:
        st.subheader(f"{stock_name} Price Chart & OHLC (Last {period} Days)")
        dates = pd.date_range(end=pd.Timestamp.today(), periods=period)
        # Simulated OHLC data: replace with real data as needed
        base = np.linspace(1800, 2200, period) + np.random.normal(0, 20, period)
        df = pd.DataFrame({
            'Date': dates,
            'Open': base + np.random.normal(2, 2, period),
            'High': base + np.random.normal(10, 3, period),
            'Low': base - np.random.normal(10, 3, period),
            'Close': base + np.random.normal(0, 3, period)
        })
        st.line_chart(df.set_index("Date")[["Close"]])
        st.dataframe(df.set_index("Date")[["Open", "High", "Low", "Close"]])

    # Always show NIFTY chart below
    st.markdown("---")
    st.subheader("NIFTY Chart Example")
    nifty_days = 30
    nifty_dates = pd.date_range(end=pd.Timestamp.today(), periods=nifty_days)
    nifty = np.linspace(19500, 20000, nifty_days) + np.random.normal(0, 25, nifty_days)
    nifty_df = pd.DataFrame({"Date": nifty_dates, "NIFTY": nifty})
    st.line_chart(nifty_df.set_index("Date")["NIFTY"])

elif section == "Research Reports":
    st.header("Research Reports")
    st.write("Get detailed financial research and AI-curated insight here.")

elif section == "Option Trading AI":
    st.header("Option Trading AI")
    st.write("Explore AI-powered strategies, risk analysis, and visuals.")

elif section == "Chart Analysis":
    st.header("Chart Analysis")
    st.write("Market data visualization - indicators, trends, and more.")

# Dark theme tweaks (optional)
st.markdown("""
    <style>
    .css-1d391kg {background-color: #222 !important;}
    .css-18e3th9 {background-color: #181818 !important;}
    header.st-emotion-cache-18ni7ap {background: #222 !important;}
    </style>
""", unsafe_allow_html=True)
