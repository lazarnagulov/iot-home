import random
import threading
import time
from typing import Generator

from config import IRConfig
from util.event_bus import EventBus, SensorEvent

def generate_ir_signal(prob_motion: float = 0.1) -> Generator[int, None, None]:
    while True:
        yield 1 if random.random() < prob_motion else 0

def run_ir_bedroom_simulator(
    config: IRConfig,
    delay: float,
    event_bus: EventBus,
    stop_event: threading.Event,
    pause_event: threading.Event = threading.Event()
) -> None:
    for signal in generate_ir_signal():
        time.sleep(delay)
        if not pause_event.is_set():
            event_bus.publish(
                SensorEvent(
                    device_info=config,
                    value={"motion": signal}
                )
            )
        if stop_event.is_set():
            break
