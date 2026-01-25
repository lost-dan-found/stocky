from textual.app import App, ComposeResult
from textual.widgets import Static


class DashboardApp(App):

    CSS = """
    Screen {
        layout: grid;
        grid-size: 3 3;          /* 3 columns, 3 rows */
        grid-columns: 1fr 1fr 1fr;
        grid-rows: 1fr 1fr 1fr;
        background: transparent;
    }

    .box {
        border: white;
        background: transparent;
        content-align: center middle;
        padding: 1 1;
        width: 100%;
        height: 100%;
    }

    /* ---- Grid Placement ---- */

    #stock1 { grid-columns: 1; grid-rows: 1; }   /* X */
    #stock2 { grid-columns: 1; grid-rows: 2; }   /* X */

    #big { grid-columns: 2; grid-rows: 1; column-span: 2; row-span: 2; }  /* OO / OO */

    #stock3 { grid-columns: 1; grid-rows: 3; }   /* X */
    #stock4 { grid-columns: 2; grid-rows: 3; }   /* X */
    #stock5 { grid-columns: 3; grid-rows: 3; }   /* X */
    """

    BINDINGS = [("ctrl+l", "open_location_prompt", "Set Location")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ansi_color = True

    def compose(self) -> ComposeResult:
        # Left column (top)
        self.stock1 = Static("Placeholder Stock 1", id="stock1", classes="box")
        self.stock1.border_subtitle = "TSLA"

        self.stock2 = Static("Placeholder Stock 2", id="stock2", classes="box")
        self.stock2.border_subtitle = "DANK"

        # Big 2x2 box
        self.big = Static("Placeholder Big Panel", id="big", classes="box")
        self.big.border_subtitle = "META"

        # Bottom row
        self.stock3 = Static("Placeholder Stock 3", id="stock3", classes="box")
        self.stock3.border_subtitle = "AAPL"

        self.stock4 = Static("Placeholder Stock 4", id="stock4", classes="box")
        self.stock4.border_subtitle = "MSFT"

        self.stock5 = Static("Placeholder Stock 5", id="stock5", classes="box")
        self.stock5.border_subtitle = "BTCN"

        yield self.stock1
        yield self.big
        yield self.stock2
        yield self.stock3
        yield self.stock4
        yield self.stock5


if __name__ == "__main__":
    DashboardApp().run()
