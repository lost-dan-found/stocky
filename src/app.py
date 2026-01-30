from textual.containers import VerticalScroll
from textual.widgets import Button
from textual.app import App, ComposeResult
from widget import StockPlot   # the class above

class DashboardApp(App):

    CSS = """
    Screen {
        layout: grid;
        grid-size: 4 4;
        grid-columns: 1fr 1fr 1fr 1fr;
        grid-rows: 1fr 1fr 1fr 1fr;
    }

    .box {
        border: white;
        padding: 1 1;
        width: 100%;
        height: 100%;
    }

    #stock1 { grid-columns: 1; grid-rows: 1; }
    #stock2 { grid-columns: 1; grid-rows: 2; }
    #big    { grid-columns: 2; grid-rows: 1; column-span: 3; row-span: 3; }
    #stock3 { grid-columns: 1; grid-rows: 3; }
    #stock4 { grid-columns: 2; grid-rows: 3; }
    #stock5 { grid-columns: 3; grid-rows: 3; }
    """

    BINDINGS = [("ctrl+l", "open_location_prompt", "Set Location")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ansi_color = True

    def compose(self) -> ComposeResult:

        # with VerticalScroll():
        #     yield Button("Button 1")

        
        yield StockPlot("TSLA", id="stock1", classes="box")
        yield StockPlot("META", id="big", classes="box")
        yield StockPlot("APLE", id="stock2", classes="box")
        yield StockPlot("GOOG", id="stock3", classes="box")
        yield StockPlot("AMZN", id="stock4", classes="box")
        yield StockPlot("MSFT", id="stock5", classes="box")


if __name__ == "__main__":
    DashboardApp().run()
