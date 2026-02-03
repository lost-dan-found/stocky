from textual.containers import VerticalScroll
from textual.widgets import Button
from textual.app import App, ComposeResult
from widget import StockPlot, StockInfo
from modal import AddStockModal

class Stocky(App):

    CSS = """
    Screen {
        layout: grid;
        grid-size: 4 4;
        background: transparent;
    }

    #sidebar {
        row-span: 4;
        padding: 0;
        scrollbar-size: 0 0;
        scrollbar-visibility: hidden;
        scrollbar-color-active: white;
        background: transparent;
    }

    .sidebar-plot, #add_stock_button {
        height: 25%;
        width: 100%;
        border: solid white;
        background: transparent;
    }
    
    .sidebar-plot:hover, #add_stock_button:hover {
        border: solid white;
    }

    #display {
        column-span: 3;
        row-span: 3;
        border: solid white;
        padding: 0;
        background: transparent;
    }

    #stock_info {
        column-span: 3;
        border: solid white;
        padding: 0 2;
        overflow-y: scroll;
        background: transparent;
    }
    """

    stocks = []
    selected_ticker = "AAPL"

    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ansi_color = True

    def compose(self) -> ComposeResult:
        
        with VerticalScroll(id="sidebar"):
            for stock in self.stocks:
                yield StockPlot(stock, classes="sidebar-plot")
            button = Button("+", id="add_stock_button")
            button.ALLOW_SELECT = False
            yield button

        yield StockPlot(self.selected_ticker, detailed=True, id="display")
        yield StockInfo(self.selected_ticker, id="stock_info")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "add_stock_button":
            self.push_screen(AddStockModal(), self.add_stock_from_modal)

    async def add_stock_from_modal(self, ticker: str):
        if ticker:
            sidebar = self.query_one("#sidebar", VerticalScroll)
            button = sidebar.query_one("#add_stock_button", Button)
            new_plot = StockPlot(ticker, classes="sidebar-plot")
            await sidebar.mount(new_plot, before = button)
            await self.select_stock(ticker)

    async def on_stock_plot_selected(self, message: StockPlot.Selected):
        await self.select_stock(message.ticker)

    async def select_stock(self, ticker: str):
        self.selected_ticker = ticker

        # Update main chart
        main_chart = self.query_one("#display", StockPlot)
        await main_chart.update_ticker(ticker)

        # Update info
        info_panel = self.query_one("#stock_info", StockInfo)
        info_panel.ticker = ticker

if __name__ == "__main__":
    Stocky().run()
