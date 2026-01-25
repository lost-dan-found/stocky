import yfinance as yf
import pandas as pd


def get_stock_history(ticker):
    data = yf.download(
        ticker,
        period="1mo",
        interval="1d",
        progress=False,
        auto_adjust=True,
        threads=False,
    )

    if data.empty:
        return [], []

    # Handle multi-index columns safely
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    closes = data["Close"]

    # Ensure it's a Series
    if isinstance(closes, pd.DataFrame):
        closes = closes.iloc[:, 0]

    dates = closes.index.strftime("%d/%m/%Y").tolist()
    prices = closes.tolist()

    return dates, prices
