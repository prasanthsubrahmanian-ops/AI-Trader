import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide", initial_sidebar_state="expanded")

# Sidebar Navigation and Inputs
st.sidebar.markdown("## 📂 Navigation")
section = st.sidebar.radio(
    "Go to", 
    ["Home", "Research Reports", "Option Trading AI", "Chart Analysis"]
)

st.sidebar.markdown("---")
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

    st.markdown("### Market Trends")

    # Sidebar for user input (stock, price type, period)
    st.sidebar.markdown("### Select Stock & Price")
    stock_symbol = st.sidebar.selectbox("Stock Name", ["TCS", "RELIANCE", "INFY", "NIFTY"])
    price_type = st.sidebar.selectbox("Price Type", ["Close", "Open", "High", "Low"])
    num_days = st.sidebar.slider("Number of Days", 10, 60, 30)

    # Simulate sample data
    dates = pd.date_range(end=pd.Timestamp.today(), periods=num_days)
    np.random.seed(42)
    # This part simulates different price types for illustration
    price_base = np.linspace(3000, 3500, num=num_days)
    df = pd.DataFrame({
        "Date": dates,
        "Close": price_base + np.random.normal(0, 10, size=num_days),
        "Open": price_base + np.random.normal(0, 15, size=num_days),
        "High": price_base + 10 + np.random.normal(0, 5, size=num_days),
        "Low": price_base - 10 + np.random.normal(0, 5, size=num_days),
    })
    st.line_chart(df.set_index('Date')[[price_type]])

elif section == "Research Reports":
    st.header("Research Reports")
    st.write("Get detailed financial research and AI-curated insight here.")

elif section == "Option Trading AI":
    st.header("Option Trading AI")
    st.write("Explore AI-powered strategies, risk analysis, and visuals.")

elif section == "Chart Analysis":
    st.header("Chart Analysis")
    st.write("Market data visualization - indicators, trends, and more.")

# Optional: Small CSS tweaks for dark theme enhancements
st.markdown("""
    <style>
    .css-1d391kg {background-color: #222 !important;}
    .css-18e3th9 {background-color: #181818 !important;}
    header.st-emotion-cache-18ni7ap {background: #222 !important;}
    </style>
""", unsafe_allow_html=True)
