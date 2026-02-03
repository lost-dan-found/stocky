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
    
    .sidebar-plot:hover, #add_stock_button:hover, .sidebar-plot:focus, #add_stock_button:focus {
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
        content-align: center middle;
        column-span: 3;
        border: solid white;
        padding: 0 0;
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
        
        with VerticalScroll(id="sidebar") as sidebar:
            sidebar.can_focus = False
            for stock in self.stocks:
                yield StockPlot(stock, classes="sidebar-plot")
            button = Button("+", id="add_stock_button")
            button.can_focus = False
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

    async def on_stock_plot_delete(self, message: StockPlot.Delete):
        widget = message.plot
        ticker = message.ticker
        
        # If we are deleting the currently selected stock, try to select another one
        if ticker == self.selected_ticker:
            sidebar = self.query_one("#sidebar")
            plots = list(sidebar.query(StockPlot))
            
            next_ticker = None
            if widget in plots:
                idx = plots.index(widget)
                # Try to pick the one after, or the one before
                if idx + 1 < len(plots):
                    next_ticker = plots[idx + 1].ticker
                elif idx - 1 >= 0:
                    next_ticker = plots[idx - 1].ticker
            
            if next_ticker:
                await self.select_stock(next_ticker)
                # Focus the new selection
                for plot in sidebar.query(StockPlot):
                    if plot.ticker == next_ticker:
                        plot.focus()
                        break
            else:
                # No stocks left
                self.selected_ticker = ""
                await self.select_stock("")

        await widget.remove()

if __name__ == "__main__":
    Stocky().run()
