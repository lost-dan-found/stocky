from textual.app import App, ComposeResult
from widget import StockPlot   # the class above

class DashboardApp(App):

    CSS = """
    Screen {
        layout: grid;
        grid-size: 3 3;
        grid-columns: 1fr 1fr 1fr;
        grid-rows: 1fr 1fr 1fr;
    }

    .box {
        border: white;
        padding: 1 1;
        width: 100%;
        height: 100%;
    }

    #stock1 { grid-columns: 1; grid-rows: 1; }
    #stock2 { grid-columns: 1; grid-rows: 2; }
    #big    { grid-columns: 2; grid-rows: 1; column-span: 2; row-span: 2; }
    #stock3 { grid-columns: 1; grid-rows: 3; }
    #stock4 { grid-columns: 2; grid-rows: 3; }
    #stock5 { grid-columns: 3; grid-rows: 3; }
    """

    BINDINGS = [("ctrl+l", "open_location_prompt", "Set Location")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ansi_color = True

    def compose(self) -> ComposeResult:
        yield StockPlot("TSLA", id="stock1", classes="box")
        yield StockPlot("META", id="big", classes="box")
        yield StockPlot("TSLA", id="stock2", classes="box")
        yield StockPlot("TSLA", id="stock3", classes="box")
        yield StockPlot("MSFT", id="stock4", classes="box")
        yield StockPlot("MSFT", id="stock5", classes="box")


if __name__ == "__main__":
    DashboardApp().run()
