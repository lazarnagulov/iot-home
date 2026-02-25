import random
import threading
import time
from typing import Generator

from config import IRConfig
from util.event_bus import EventBus, SensorEvent

ir_keys = ["UP", "DOWN", "LEFT", "RIGHT", "OK", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"] 

def generate_ir_signal(prob_signal: float = 0.3) -> Generator[str | None, None, None]:
    while True:
        if random.random() < prob_signal:
            yield random.choice(ir_keys)
        else:
            yield None

def run_ir_bedroom_simulator(
    config: IRConfig,
    delay: float,
    event_bus: EventBus,
    stop_event: threading.Event,
    pause_event: threading.Event = threading.Event()
) -> None:
    for signal in generate_ir_signal():
        time.sleep(delay)
        if not pause_event.is_set() and signal is not None:
            event_bus.publish(
                SensorEvent(
                    device_info=config,
                    value={"button": signal}
                )
            )
        if stop_event.is_set():
            break
