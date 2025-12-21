import logging


class LogHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.log_panel = None
        
    def set_log_panel(self, log_panel) -> None:
        self.log_panel = log_panel
    
    def emit(self, record: logging.LogRecord) -> None:
        if self.log_panel is None:
            return
            
        try:
            msg = self.format(record)
            
            if record.levelno >= logging.ERROR:
                style = "red"
            elif record.levelno >= logging.WARNING:
                style = "yellow"
            elif record.levelno >= logging.INFO:
                style = "white"
            else:
                style = "dim"
            
            self.log_panel.add_log(msg, style=style)
        except Exception:
            self.handleError(record)