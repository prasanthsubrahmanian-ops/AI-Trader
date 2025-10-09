import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# -----------------------------
# Main App Function
# -----------------------------
def main():
    # App Title
    st.title("AI Trader App")

    # Sidebar for user inputs
    st.sidebar.header("User Inputs")
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol", "TCS")
    num_days = st.sidebar.slider("Number of Days to Predict", 1, 10, 1)

    # Load sample data (replace with real API or CSV)
    st.subheader(f"📊 Historical Data for {stock_symbol}")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    prices = np.random.randint(3000, 4000, size=(30,))
    df = pd.DataFrame({"Date": dates, "Close": prices})
    st.dataframe(df)

    # -----------------------------
    # Technical Indicators
    # -----------------------------
    st.subheader("📈 Technical Indicators")

    # Example: Moving Average
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()

    st.line_chart(df.set_index('Date')[['Close', 'MA5', 'MA10']])

    # -----------------------------
    # Next Day Prediction (Linear Regression Example)
    # -----------------------------
    st.subheader("🤖 Next Day Price Prediction")
    df['Target'] = df['Close'].shift(-1)
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['Close'].values

    model = LinearRegression()
    model.fit(X[:-1], y[:-1])

    next_day_index = np.array([[len(df)]])
    pred_next = model.predict(next_day_index)
    st.write(f"Predicted Close for next day: ₹{round(pred_next[0], 2)}")

# -----------------------------
# Run the App
# -----------------------------
if __name__ == "__main__":
    main()
