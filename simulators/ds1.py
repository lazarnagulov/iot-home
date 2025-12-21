import random
import threading
import time
from typing import Callable

def run_ds1_simulator(
    delay: int,
    callback: Callable[[], None],  
    stop_event: threading.Event
) -> None:
    while not stop_event.is_set():
        time.sleep(delay)
        if stop_event.is_set():
            break
        
        if random.uniform(0, 100) < 50:
            callback()