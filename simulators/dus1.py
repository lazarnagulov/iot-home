import random
import threading
import time
from typing import Callable, Generator

def generate_distance_value() -> Generator[float, None, None]:
    while True:
        yield random.uniform(1, 500)


def run_dus1_simulator(
    delay: int,
    callback: Callable[[float], None],  
    stop_event: threading.Event
) -> None:
    for distance in generate_distance_value():
        time.sleep(delay)
        callback(distance)
        if stop_event.is_set():
            break