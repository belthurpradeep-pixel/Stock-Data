import yfinance as yf
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Free Stock Engine is Live! 📈"}

@app.get("/ai-boom")
def ai_boom():
    # 1. Pick 5 famous stocks
    tickers = ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN"]
    
    try:
        # 2. Pull data from Yahoo Finance (FREE)
        data = yf.download(tickers, period="1d", interval="1m", group_by='ticker')
        
        stock_list = []
        for ticker in tickers:
            current_price = data[ticker]['Close'].iloc[-1]
            stock_list.append({"symbol": ticker, "price": round(current_price, 2)})

        return {
            "status": "Success",
            "market_theme": "Big Tech (Free Data Mode)",
            "stocks": stock_list,
            "ai_insight": "AI is in 'Simulation Mode'. To get real AI, add $5 to OpenAI billing."
        }
    except Exception as e:
        return {"status": "Error", "details": str(e)}