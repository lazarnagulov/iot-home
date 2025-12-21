from textual.widget import Widget
from collections import deque
from rich.text import Text


class LogPanel(Widget):
    
    def __init__(self, max_lines=100):
        super().__init__()
        self.lines = deque(maxlen=max_lines)

    def log(self, message: str):
        self.lines.appendleft(message)
        self.refresh()

    def render(self):
        text = Text()
        for line in self.lines:
            text.append(line + "\n")
        return text
