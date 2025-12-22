from textual.widgets import RichLog
from rich.text import Text
from datetime import datetime


class LogPanel(RichLog):

    def __init__(self, max_lines=10, **kwargs):
        super().__init__(max_lines=max_lines, wrap=True, highlight=True, **kwargs)

    def add_log(self, message: str, style: str = "white") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = Text()
        log_entry.append(f"[{timestamp}] ", style="dim")
        log_entry.append(message, style=style)
        self.write(log_entry)