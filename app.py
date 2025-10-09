import streamlit as st
import pandas as pd
import numpy as np

# Set page config to wide and initial sidebar state
st.set_page_config(page_title="PRASANTH AI Trading Insights", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for dark blue background and box styling, with heading moved upward nicely
st.markdown("""
    <style>
        /* Dark blue background for full page */
        .main {
            background-color: #003366;
            color: white;
            padding: 1rem 2rem;
        }
        /* Header styling - moved up, larger font, spacing */
        h1 {
            padding-top: 1rem;
            margin-bottom: 2rem;
            font-weight: 700;
            font-size: 3rem;
            text-align: center;
            color: white;
        }
        /* Boxes container with horizontal layout */
        .boxes-container {
            display: flex;
            justify-content: space-around;
            margin-bottom: 3rem;
            gap: 1rem;
            flex-wrap: wrap;
        }
        /* Each box styling */
        .box {
            background-color: #004080;
            border-radius: 12px;
            padding: 20px;
            flex: 1 1 20%;
            min-width: 200px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
            text-align: center;
            font-weight: 600;
            font-size: 1.2rem;
            cursor: pointer;
            user-select: none;
            transition: background-color 0.3s ease;
        }
        .box:hover {
            background-color: #0059b3;
        }
    </style>
    <div class="main">
        <h1>PRASANTH AI Trading Insights</h1>
        <div class="boxes-container">
            <div class="box" id="research">Research Reports</div>
            <div class="box" id="options">Options Trading</div>
            <div class="box" id="charts">Chart Analysis</div>
            <div class="box" id="ai">AI Predictions</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar inputs for stock selection and period
st.sidebar.markdown("### Stock Selection")
stock_name = st.sidebar.selectbox("Stock Name", ["TCS", "RELIANCE", "INFY", "NIFTY"])
period = st.sidebar.slider("Period (Days)", 10, 60, 30)
show_chart = st.sidebar.button("Show Price Chart")
st.sidebar.caption("Built with Streamlit | pandas | NumPy")

# Show price chart & OHLC only when button pressed
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

# Separate NIFTY section always visible
st.markdown("---")
st.subheader("NIFTY Chart Example")
nifty_days = 30
nifty_dates = pd.date_range(end=pd.Timestamp.today(), periods=nifty_days)
nifty = np.linspace(19500, 20000, nifty_days) + np.random.normal(0, 25, nifty_days)
nifty_df = pd.DataFrame({"Date": nifty_dates, "NIFTY": nifty})
st.line_chart(nifty_df.set_index("Date")["NIFTY"])
