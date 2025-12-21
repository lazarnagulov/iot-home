from textual.widget import Widget
from collections import deque
from rich.text import Text
from datetime import datetime


class LogPanel(Widget):

    def __init__(self, max_lines=100, **kwargs):
        super().__init__(**kwargs)
        self.lines = deque(maxlen=max_lines)

    def add_log(self, message: str, style: str = "white") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = Text()
        log_entry.append(f"[{timestamp}] ", style="dim")
        log_entry.append(message, style=style)
        self.lines.append(log_entry)
        self.refresh()

    def render(self) -> Text:
        if not self.lines:
            empty = Text()
            empty.append("No activity yet", style="dim italic")
            return empty
        
        text = Text()
        for line in self.lines:
            text.append(line)
            text.append("\n")
        return text