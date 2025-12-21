import logging
from textual.widgets import RichLog

class TextualLogHandler(logging.Handler):
    def __init__(self, widget: RichLog) -> None:
        super().__init__()
        self.widget = widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.widget.write(msg)