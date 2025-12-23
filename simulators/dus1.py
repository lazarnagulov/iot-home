import random
import threading
import time
from typing import Callable, Generator

from util.event_bus import EventBus, SensorEvent

def generate_distance_value() -> Generator[float, None, None]:
    while True:
        yield random.uniform(1, 500)


def run_dus1_simulator(
    delay: int,
    event_bus: EventBus,
    stop_event: threading.Event
) -> None:
    for distance in generate_distance_value():
        time.sleep(delay)
        event_bus.publish(
            SensorEvent(
                sensor="DUS1",
                payload={ "distance": f"{distance:.2f}" }
            )
        )
        if stop_event.is_set():
            break