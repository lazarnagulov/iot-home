import logging
from rich.logging import RichHandler

LOGGER_NAME = "iot_home"

def setup_logger(mode: str) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    if mode == "cli":
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [IOT Home] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

    elif mode == "tui":
        handler = RichHandler(
            show_time=False,
            show_level=False,
            rich_tracebacks=True,
        )

    else:
        raise ValueError(f"Unknown mode: {mode}")

    logger.addHandler(handler)
    return logger
