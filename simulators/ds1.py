import random
import threading
import time
from typing import Callable

from util.logger import log_message


def run_ds1_simulator(
    delay: int,
    callback: Callable[[threading.Event], None],  
    stop_event: threading.Event
) -> None:
    while not stop_event.is_set():
        log_message("Checking door sensor...")
        time.sleep(delay)
        if stop_event.is_set():
            break
        
        if random.uniform(0, 100) < 50:
            callback(stop_event)