import yfinance as yf

# get daily data for Apple
data = yf.download("AAPL", start="2020-01-01", end="2025-01-01")
print(data.head())