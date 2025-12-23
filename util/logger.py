import logging
from rich.logging import RichHandler
from typing import Optional

from app.tui.loging_handler import LogHandler

LOGGER_NAME = "iot_home"

_tui_handler: Optional[LogHandler] = None


def setup_logger(mode: str, level: int = logging.INFO) -> logging.Logger:
    global _tui_handler
    
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.handlers.clear()

    if mode == "cli":
        handler = RichHandler(
            show_time=True,
            show_level=True,
            show_path=False,
            rich_tracebacks=True,
            markup=True,
        )
        formatter = logging.Formatter(
            "%(message)s",
            datefmt="[%X]",
        )
        handler.setFormatter(formatter)

    elif mode == "tui":
        _tui_handler = LogHandler()
        handler = _tui_handler
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)

    else:
        raise ValueError(f"Unknown mode: {mode}")

    logger.addHandler(handler)
    logger.propagate = False  
    
    return logger


def get_tui_handler() -> Optional[LogHandler]:
    return _tui_handler


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)