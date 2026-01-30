import asyncio
import yfinance as yf
import pandas as pd

_download_lock = asyncio.Lock()

async def get_stock_history_threadsafe(ticker):
    async with _download_lock:
        return await asyncio.to_thread(_get_stock_history_sync, ticker)

def _get_stock_history_sync(ticker):
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

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    closes = data["Close"]

    if isinstance(closes, pd.DataFrame):
        closes = closes.iloc[:, 0]

    dates = closes.index.strftime("%d/%m/%Y").tolist()
    prices = closes.tolist()

    return dates, prices
