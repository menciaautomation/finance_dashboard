import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
plt.style.use('dark_background')


# Page title
st.title("Stock Data Dashboard")

# Sidebar inputs
st.sidebar.header("Stock Selection")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker", value="MSFT")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-12-31"))
ma_window = st.sidebar.slider("Moving Average Window", min_value=5, max_value=50, value=20)

# Fetching data
st.write(f"Data for **{ticker_symbol}** from **{start_date}** to **{end_date}**")
data = yf.download(ticker_symbol, start=start_date, end=end_date)

if data.empty:
    st.error("No data found. Please check the ticker symbol or date range.")
    st.stop()

# Calculate moving average
data["MA"] = data["Close"].rolling(window=ma_window).mean()

# Initialize Tabs
tabs = st.tabs(["📄 Raw Data", "💵 Price Chart", "📊 Volume Chart", "📈 Moving Average"])

# --- Tab 1: Raw Data ---
with tabs[0]:
    st.subheader(f"Raw Data for {ticker_symbol}")
    st.write(data.tail())
    st.download_button("Download Data as CSV", data.to_csv().encode("utf-8"), f"{ticker_symbol}_data.csv")

# --- Tab 2: Price Chart ---
with tabs[1]:
    st.subheader(f"Price Chart for {ticker_symbol}")
    st.line_chart(data["Close"])

# --- Tab 3: Volume Chart ---
with tabs[2]:
    st.subheader(f"Volume Chart for {ticker_symbol}")
    st.line_chart(data["Volume"])

# --- Tab 4: Moving Average ---
with tabs[3]:
    st.subheader(f"Moving Average Chart ({ma_window}-Day) for {ticker_symbol}")

    # Create figure + axis
    fig, ax = plt.subplots()

    # Make background transparent so it blends with Streamlit dark mode
    fig.patch.set_alpha(0)       # outer figure background
    ax.set_facecolor("none")     # inner plot background

    # Plot your data
    ax.plot(data.index, data["Close"], label="Closing Price", color="#3c93d2", linewidth=1.5)
    ax.plot(data.index, data["MA"], label=f"{ma_window}-Day MA", color="orange", linewidth=1.3)

    # Add legend + labels
    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")

    # Display it in Streamlit
    st.pyplot(fig)


