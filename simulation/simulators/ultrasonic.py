import random
import threading
import time
from typing import Generator

from config import UltrasonicConfig
from util.event_bus import EventBus, SensorEvent

def generate_distance_value() -> Generator[float, None, None]:
    while True:
        yield random.uniform(1, 500)


def run_ultrasonic_simulator(
    config: UltrasonicConfig,
    delay: int,
    event_bus: EventBus,
    stop_event: threading.Event
) -> None:
    for distance in generate_distance_value():
        time.sleep(delay)
        event_bus.publish(
            SensorEvent(
                device_info=config,
                value={ "distance": round(distance, 4) }
            )
        )
        if stop_event.is_set():
            break