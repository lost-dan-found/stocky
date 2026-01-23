from textual.app import App, ComposeResult
from textual.widgets import Digits, Static, Input
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical

class DashboardApp(App):
    CSS = """
    Screen {
        background: transparent;
    }

    .box {
        border: white;
        background: transparent;
        content-align: center middle;
        padding: 1 1;
    }

    #top_left {
        width: 33%;
        height: 100%;
    }

    #top_right {
        width: 66%;
        height: 100%;
    }

    #top_row {
        width: 100%;
        height: 66%;
    }

    #stock_1 {
        width: 100%;
        height: 50%;
    }

    #stock_2 {
        width: 100%;
        height: 50%;
    }

    #stock_3 {
        width: 33%;
        height: 100%;
    }

    #stock_4 {
        width: 33%;
        height: 100%;
    }

    #stock_5 {
        width: 33%;
        height: 100%;
    }

    #stock_6 {
        width: 100%;
        height: 100%;
    }

    #bottom_row {
        width: 100%;
        height: 33%;
    }
    """

    #add a key binding to open the location prompt
    BINDINGS = [("ctrl+l", "open_location_prompt", "Set Location")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ansi_color = True

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="top_row"):
                with Vertical(id="top_left"):
                    with Vertical():
                        self.stock1 = Static("Stock 1", id="stock_1", classes="box")
                        self.stock2 = Static("Stock 2", id="stock_2", classes="box")

                        yield self.stock1
                        yield self.stock2
                with Vertical(id="top_right"):
                    self.stock6 = Static("Stock 6", id="stock_6", classes="box")
                    yield self.stock6
            with Horizontal(id="bottom_row"):
                self.stock3 = Static("Stock 3", id="stock_3", classes="box")
                self.stock4 = Static("Stock 4", id="stock_4", classes="box")
                self.stock5 = Static("Stock 5", id="stock_5", classes="box")
                
                yield self.stock3
                yield self.stock4
                yield self.stock5


if __name__ == "__main__":
    DashboardApp().run()
