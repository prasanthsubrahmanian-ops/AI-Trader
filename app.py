import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide")

st.markdown("""
<style>
body, .main, .block-container {
    background-color: #002258 !important;
    color: #fff !important;
}
.sidebar .sidebar-content, .css-fblp2m {
    background-color: #143364 !important;
}
.user-panel { 
    text-align: center; 
    margin-bottom: 1rem;
}
.user-avatar { 
    border-radius: 50%; 
    width: 60px; 
    margin-bottom: .7rem; 
}
.nav-menu { 
    text-align: left; 
    margin-top: 1.25rem; 
}
.nav-link { 
    color: #fff; 
    font-weight: 600; 
    font-size: 1.12rem; 
    margin-bottom: 1rem; 
    display: block; 
    text-decoration: none; 
}
.nav-link:hover { color: #ffda3a; }
.header-text { 
    margin-top: 1.5rem; 
    color: #fff; 
    font-size: 2.3rem; 
    font-weight: 700; 
    padding-left: .5rem; 
    margin-bottom: 1.8rem; 
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="user-panel">', unsafe_allow_html=True)
    st.image('https://randomuser.me/api/portraits/men/32.jpg', width=60)
    st.markdown('<b>John Don</b>', unsafe_allow_html=True)
    st.markdown('john@sharetrading.com')
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-menu">', unsafe_allow_html=True)
    st.markdown('<a class="nav-link">Home</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link">Research Reports</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link">Options Trading</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link">Chart Analysis</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link">AI Predictions</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="header-text">PRASANTH AI Trading Insights</div>', unsafe_allow_html=True)

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
