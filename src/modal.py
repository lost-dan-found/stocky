from textual.containers import Vertical
from textual.widgets import Input, Label
from textual.app import ComposeResult
from textual.screen import ModalScreen

class AddStockModal(ModalScreen[str]):
    """Screen with a dialog to add a stock."""

    CSS = """
    AddStockModal {
        align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        padding: 0 1;
        width: 60;
        height: 10;
        border: round white;
        background: $surface;
    }

    #question {
        column-span: 2;
        height: 1fr;
        width: 100%;
        content-align: center middle;
    }

    Input {
        column-span: 2;
        margin: 1 0;
    }
    """

    BINDINGS = [("escape", "dismiss", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Select a stock:", id="question")
            yield Input(placeholder="e.g., AAPL")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value.strip().upper())