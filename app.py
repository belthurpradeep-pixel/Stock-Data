import streamlit as st
import yfinance as yf
import pandas as pd

# 1. SETUP PAGE
st.set_page_config(page_title="Stock-AI Dashboard", layout="wide")
st.title("🚀 Real-Time Stock AI Dashboard")

# 2. SIDEBAR SEARCH
st.sidebar.header("Stock Explorer")
search_symbol = st.sidebar.text_input("🔍 Search Symbol (e.g. NVDA, AAPL, BTC-USD):", "").upper()

if search_symbol:
    try:
        ticker = yf.Ticker(search_symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = data['Close'].iloc[-1]
            st.metric(label=f"Current Price: {search_symbol}", value=f"${round(price, 2)}")
            # Display a small chart
            hist = ticker.history(period="7d")
            st.line_chart(hist['Close'])
        else:
            st.sidebar.error("No data found.")
    except Exception as e:
        st.sidebar.error("Error fetching data.")

st.markdown("---")

# 3. TOP MARKET LEADERS (Direct from Yahoo Finance)
st.subheader("🔥 Top 5 Market Leaders (Real-Time)")
tickers = ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN"]

@st.cache_data(ttl=60)
def get_live_prices():
    # This replaces the 'Uvicorn Engine' by getting data directly
    data = yf.download(tickers, period="1d", interval="1m", group_by='ticker')
    prices = {t: round(data[t]['Close'].iloc[-1], 2) for t in tickers}
    return prices

try:
    current_prices = get_live_prices()
    cols = st.columns(5)
    for i, ticker in enumerate(tickers):
        cols[i].metric(label=ticker, value=f"${current_prices[ticker]}")
except Exception as e:
    st.warning("Market is loading... click refresh if blank.")

st.info("💡 Note: This app is now running 'Serverless' directly on Streamlit Cloud!")
