import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Trader Dashboard", layout="wide", initial_sidebar_state="expanded")

# Sidebar - Navigation
st.sidebar.markdown("## 📂 Navigation")
menu = st.sidebar.radio(
    "Go to", 
    ["Home", "Research Reports", "Option Trading AI", "Chart Analysis"],
    key="section"
)

# Optional: Add user panel
with st.sidebar.expander("👤 User Profile", expanded=False):
    st.image("https://randomuser.me/api/portraits/men/75.jpg", width=60)
    st.markdown("**James Gibson**")
    st.markdown("Premium Member")

st.sidebar.markdown("---")
st.sidebar.write("Data powered by Pandas, NumPy, and AI.")

# TOP HEADER
st.markdown("""
    <div style="background-color:#1565c0;padding:28px 0 18px 0; border-radius:16px;margin-bottom:32px;">
        <h1 style="color:white;text-align:center; margin:0;">
            <span style="font-size:2.0rem;vertical-align:middle;">💹</span>
            <span style="vertical-align:middle;font-size:2.7rem;">AI Trader Dashboard</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

if menu == "Home":
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📊 Research Reports")
        st.write("Detailed market analysis and AI-curated research for informed decision-making.")
    with col2:
        st.markdown("#### 🧠 Option Trading AI")
        st.write("AI-generated option strategies, risk visuals, and chain analysis tools.")
    with col3:
        st.markdown("#### 📈 Chart Analysis")
        st.write("Visualize live market data with interactive charts and indicators.")

    st.markdown("---")
    st.markdown("### Key Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Today Views", "52,409", "+830")
    c2.metric("Active Users", "1,210", "+19")
    c3.metric("Profit (₹)", "89,000", "+3%")

    st.markdown("### Market Trends Example")
    # Historical Data Section with moving averages
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    prices = np.random.randint(3200, 3700, size=(30,))
    df = pd.DataFrame({"Date": dates, "Close": prices})
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    st.line_chart(df.set_index('Date')[['Close', 'MA5', 'MA10']])

elif menu == "Research Reports":
    st.header("Research Reports")
    st.write("Get detailed financial research and AI-curated insight here.")
    # Add your custom report charts, tables, analysis here

elif menu == "Option Trading AI":
    st.header("Option Trading AI")
    st.write("Explore AI-powered strategies, risk analysis, and visuals.")
    # Insert your option chain chart, stats, etc.

elif menu == "Chart Analysis":
    st.header("Chart Analysis")
    st.write("Market data visualization - indicators, trends, and more.")
    # Insert dynamic charting and metrics here

# Style tweaks for dark theme (optional)
st.markdown("""
    <style>
    .css-1d391kg {background-color: #222 !important;}
    .css-18e3th9 {background-color: #181818 !important;}
    header.st-emotion-cache-18ni7ap {background: #222 !important;}
    </style>
""", unsafe_allow_html=True)
