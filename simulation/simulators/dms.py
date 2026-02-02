import random
import threading
import time
from typing import Generator

from util.event_bus import EventBus, SensorEvent

def generate_random_key() -> Generator[str, None, None]:
    while True:
        yield random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '*', '#', 'A', 'B', 'C', 'D'], 1)[0]


def run_dms_simulator(
    delay: int,
    event_bus: EventBus,
    stop_event: threading.Event
) -> None:
    for key in generate_random_key():
        time.sleep(delay)
        event_bus.publish(
            SensorEvent(
                sensor="DMS",
                payload={ "last_key": f"{ key }" }
            )
        )
        if stop_event.is_set():
            break