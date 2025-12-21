
import threading
import time
from typing import List

from components.ds1 import run_ds1
from components.dus1 import run_dus1
from config import Config, load_config
from util.logger import log_message

try:
    import RPi.GPIO as GPIO # ty: ignore[unresolved-import]
    GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError:
    pass


def main() -> None:
    log_message('Starting app...')
    config: Config = load_config()
    threads: List[threading.Thread] = []
    stop_event: threading.Event = threading.Event()
    try:
        run_ds1(config.ds1_config, threads, stop_event)
        run_dus1(config.dus1_config, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        log_message('Stopping app')
        for t in threads:
            stop_event.set()
    

if __name__ == "__main__":
    main()