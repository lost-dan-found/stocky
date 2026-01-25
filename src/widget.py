from textual_plotext import PlotextPlot
from textual.widget import Widget
import asyncio
from util import get_stock_history  # your function


class StockPlot(PlotextPlot):

    def __init__(self, ticker: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticker = ticker
        self.border_subtitle = ticker

    async def on_mount(self):
        await self.load_data()

    async def load_data(self):
        # run blocking yfinance in a thread
        dates, prices = await asyncio.to_thread(get_stock_history, self.ticker)

        self.plt.clear_data()
        self.plt.plot(dates, prices)
        self.plt.title(self.ticker)
        self.refresh()
