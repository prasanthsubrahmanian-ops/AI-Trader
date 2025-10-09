import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Trader Dashboard", layout="wide", initial_sidebar_state="expanded")

# Sidebar Navigation
st.sidebar.markdown("## 📂 Navigation")
section = st.sidebar.radio(
    "Go to", 
    ["Home", "Research Reports", "Option Trading AI", "Chart Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit | pandas | NumPy")

# Top Header
st.markdown("""
    <div style="background-color:#1565c0;padding:28px 0 18px 0; border-radius:16px;margin-bottom:32px;">
        <h1 style="color:white;text-align:center; margin:0;">
            <span style="font-size:2.0rem;vertical-align:middle;">💹</span>
            <span style="vertical-align:middle;font-size:2.7rem;">AI Trader Dashboard</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

if section == "Home":
    # Custom info cards for shares, period, values
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🔄 Shares")
        st.write("75%")
    with col2:
        st.markdown("#### ⏳ Period")
        st.write("Last 30 days")
    with col3:
        st.markdown("#### 💲 Values")
        st.write("340,108")  # Sample value; replace with real data or a dynamic fetch

    st.markdown("---")
    st.markdown("### Market Trends (Nifty Example)")

    # Simulated Nifty historical data
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    prices = np.random.randint(19500, 20300, size=(30,))
    df = pd.DataFrame({"Date": dates, "Nifty": prices})
    df['MA5'] = df['Nifty'].rolling(window=5).mean()
    df['MA10'] = df['Nifty'].rolling(window=10).mean()
    st.line_chart(df.set_index('Date')[['Nifty', 'MA5', 'MA10']])

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
