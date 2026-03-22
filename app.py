import streamlit as st
import requests
import pandas as pd

# --- STYLING ---
st.set_page_config(page_title="Multibagger AI", layout="wide")
st.title("🚀 Multibagger-Lite: AI Stock Discovery")
# --- SEARCH BAR ---
search_symbol = st.text_input("🔍 Search for a Stock (e.g., TSLA, GOOG, NFLX):", "").upper()

if search_symbol:
    try:
        # Fetch data for the searched stock
        ticker_data = yf.Ticker(search_symbol)
        price = ticker_data.history(period="1d")['Close'].iloc[-1]
        st.success(f"The current price of **{search_symbol}** is **${round(price, 2)}**")
    except:
        st.error("Could not find that symbol. Please try a valid Ticker.")
        
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("Settings")
if st.sidebar.button("Refresh Market Data"):
    st.rerun()

# --- MAIN DASHBOARD ---
st.subheader("🔥 Top 5 Market Leaders (Real-Time)")

# Fetch data from your FastAPI engine
try:
    response = requests.get("http://127.0.0.1:8000/ai-boom")
    data = response.json()
    
    if data["status"] == "Success":
        # Create a nice table
        df = pd.DataFrame(data["stocks"])
        
        # Display as beautiful metric cards
        cols = st.columns(5)
        for i, stock in enumerate(data["stocks"]):
            cols[i].metric(label=stock["symbol"], value=f"${stock['price']}")
        
        st.markdown("### 🤖 AI Market Insight")
        st.info(data["ai_insight"])
        
        st.write("Raw Data Table:")
        st.table(df)
    else:
        st.error("Engine is sleeping. Make sure main.py is running!")
except:
    st.warning("Waiting for Engine... (Did you run 'uvicorn main:app' in the other terminal?)")

st.markdown("---")
st.caption("Powered by Yahoo Finance & FastAPI")