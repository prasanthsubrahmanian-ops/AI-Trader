import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Trader", layout="wide")

# -----------------------------
# CUSTOM CSS (Blue Theme + Cards)
# -----------------------------
st.markdown("""
    <style>
        body {
            background-color: #f6f9fc;
            color: #1a1a1a;
        }
        .main-title {
            background-color: #0059b3;
            color: white;
            text-align: center;
            padding: 25px 10px;
            font-size: 40px;
            font-weight: bold;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .section-header {
            color: #0059b3;
            font-size: 26px;
            font-weight: 600;
            border-left: 6px solid #0073e6;
            padding-left: 10px;
            margin-top: 40px;
            margin-bottom: 10px;
        }
        .card {
            background-color: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            text-align: center;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card-title {
            color: #0073e6;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: #666;
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Research Reports", "Option Trading AI", "Chart Analysis"])

# -----------------------------
# HOME PAGE
# -----------------------------
if page == "Home":
    st.markdown("<div class='main-title'>💹 AI Trader Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Overview</div>", unsafe_allow_html=True)
    st.write("Your one-stop dashboard for AI-driven financial insights, trading tools, and analytics.")

    # Feature cards (3 columns)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>📊 Research Reports</div>
            <p>Get detailed market analysis and AI-curated research insights for informed decision-making.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>🧠 Option Trading AI</div>
            <p>Discover AI-generated strategies, option chain visualizations, and risk analysis tools.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>📈 Chart Analysis</div>
            <p>Visualize live market data with clean charts, indicators, and price action analysis.</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# RESEARCH REPORTS PAGE
# -----------------------------
elif page == "Research Reports":
    st.markdown("<div class='main-title'>📊 Research Reports</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Market Overview</div>", unsafe_allow_html=True)
    st.write("This section will feature AI-generated market summaries, company insights, and sector analysis.")
    st.info("Coming soon: Auto-generated PDFs and research uploads.")

# -----------------------------
# OPTION TRADING AI PAGE
# -----------------------------
elif page == "Option Trading AI":
    st.markdown("<div class='main-title'>🧠 Option Trading AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>AI Strategy Center</div>", unsafe_allow_html=True)
    st.write("This area will host live option chain data and AI-driven strategy recommendations.")
    st.warning("Coming soon: Backtesting and prediction models.")

# -----------------------------
# CHART ANALYSIS PAGE
# -----------------------------
elif page == "Chart Analysis":
    st.markdown("<div class='main-title'>📈 Chart Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Technical Charts</div>", unsafe_allow_html=True)
    st.write("Analyze market trends with candlestick charts and moving averages.")
    st.success("Coming soon: Live charts and pattern recognition AI.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("<div class='footer'>🚀 Built with Streamlit | Designed by Finser | Blue Theme Edition</div>", unsafe_allow_html=True)