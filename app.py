import streamlit as st
import yfinance as yf
import pandas as pd

# 1. PAGE SETTINGS
st.set_page_config(page_title="Multibagger AI", layout="wide")
st.title("🚀 Multibagger AI: Live Dashboard")

# 2. SEARCH BAR (The New Brain)
st.sidebar.header("Stock Explorer")
search_symbol = st.sidebar.text_input("🔍 Search Symbol (e.g. NVDA, BTC-USD):", "").upper()

if search_symbol:
    try:
        ticker = yf.Ticker(search_symbol)
        # Fetch the very last closing price
        data = ticker.history(period="1d")
        if not data.empty:
            price = data['Close'].iloc[-1]
            st.metric(label=f"Current Price of {search_symbol}", value=f"${round(price, 2)}")
            
            # Show a small trend chart
            hist = ticker.history(period="7d")
            st.line_chart(hist['Close'])
        else:
            st.sidebar.error("No data found for this symbol.")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

st.markdown("---")

# 3. TOP LEADERS SECTION
st.subheader("🔥 Market Leaders (Real-Time)")
tickers = ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN"]

@st.cache_data(ttl=60) # Refreshes every minute
def get_market_data():
    # This downloads all 5 stocks at once
    data = yf.download(tickers, period="1d", interval="1m", group_by='ticker')
    results = {}
    for t in tickers:
        results[t] = round(data[t]['Close'].iloc[-1], 2)
    return results

try:
    prices = get_market_data()
    cols = st.columns(5)
    for i, ticker in enumerate(tickers):
        cols[i].metric(label=ticker, value=f"${prices[ticker]}")
except Exception as e:
    st.error("Market data is waking up... try refreshing in a moment.")

st.info("💡 Note: This app is now running 'Serverless' directly on Streamlit Cloud!")
