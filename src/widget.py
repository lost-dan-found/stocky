from textual_plotext import PlotextPlot
from textual.widget import Widget
import asyncio
from util import get_stock_history  # your function

class StockPlot(PlotextPlot):

    def __init__(self, ticker: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticker = ticker
        self.ansi_color = True
        self.border_subtitle = ticker

    async def on_mount(self):
        await self.load_data()

    async def load_data(self):
        x, prices = await asyncio.to_thread(get_stock_history, self.ticker)

        if not x or not prices:
            return

        self.plt.clear_figure()

        # Make plot “transparent”
        
        self.plt.canvas_color("default")
        self.plt.axes_color("default")
        self.plt.ticks_color("default")
        self.plt.frame(False)
        self.plt.grid(False)

        # Decide line color
        color = "green" if prices[-1] >= prices[0] else "red"

        # Draw the line
        self.plt.plot(x, prices, color=color, marker="braille")

        # Optional: minimal ticks for readability
        self.plt.xticks(x[::max(1, len(x)//5)])

        self.plt.theme("clear")

        self.refresh()