from textual.message import Message
from textual.widgets import Static
from textual.reactive import reactive
from textual_plotext import PlotextPlot
from util import get_stock_history_threadsafe, get_stock_info_threadsafe

class StockPlot(PlotextPlot):

    class Selected(Message):
        def __init__(self, ticker: str):
            self.ticker = ticker
            super().__init__()

    class Delete(Message):
        def __init__(self, plot, ticker: str):
            self.plot = plot
            self.ticker = ticker
            super().__init__()

    BINDINGS = [
        ("enter,space", "select", "Select"),
        ("delete,backspace", "delete", "Delete"),
    ]

    def __init__(self, ticker: str, detailed: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticker = ticker
        self.detailed = detailed
        self.border_subtitle = ticker
        self.ALLOW_SELECT = False
        if not detailed:
            self.can_focus = True

    async def on_click(self):
        self.post_message(self.Selected(self.ticker))

    def action_select(self):
        self.post_message(self.Selected(self.ticker))

    def action_delete(self):
        if not self.detailed:
            self.post_message(self.Delete(self, self.ticker))

    async def on_focus(self):
        if not self.detailed:
            self.post_message(self.Selected(self.ticker))

    async def on_mount(self):
        await self.load_data()

    async def update_ticker(self, ticker: str):
        self.ticker = ticker
        self.border_subtitle = ticker
        await self.load_data()

    async def load_data(self):
        x, prices = await get_stock_history_threadsafe(self.ticker)

        if not x or not prices:
            self.plt.clear_figure()
            self.refresh()
            return

        self.plt.clear_figure()

        # Make plot “transparent”
        
        self.plt.canvas_color("default")
        self.plt.axes_color("default")
        self.plt.ticks_color("default")

        if self.detailed:
            self.plt.frame(False)
            self.plt.grid(False)
            self.plt.title(f"{self.ticker} Price History")
        else:
            self.plt.frame(False)
            self.plt.grid(False)

        # Decide line color
        color = "green" if prices[-1] >= prices[0] else "red"

        # Draw the line
        self.plt.plot(x, prices, color=color, marker="braille")

        # Optional: minimal ticks for readability
        if not self.detailed:
            self.plt.xticks([])
            self.plt.yticks([])
            
        self.plt.theme("clear")

        self.refresh()

class StockInfo(Static):
    ticker = reactive("")

    def __init__(self, ticker: str = "", **kwargs):
        super().__init__(**kwargs)
        self.ticker = ticker

    async def on_mount(self):
        if self.ticker:
            await self.load_info()

    async def watch_ticker(self, new_ticker):
        if new_ticker:
            await self.load_info()

    async def load_info(self):
        if not self.ticker:
            self.update("Select a stock to view details.")
            return

        self.update(f"Loading data for {self.ticker}...")
        info = await get_stock_info_threadsafe(self.ticker)
        
        if not info:
            self.update(f"Could not load info for {self.ticker}")
            return

        name = info.get("shortName", self.ticker)
        sector = info.get("sector", "Unknown Sector")
        price = info.get("currentPrice", "N/A")
        currency = info.get("currency", "USD")
        summary = info.get("longBusinessSummary", "No summary available.")
        
        content = f"""
# {name} ({self.ticker})
**Price:** {price} {currency}  |  **Sector:** {sector}

---
{summary}
"""
        self.update(content)