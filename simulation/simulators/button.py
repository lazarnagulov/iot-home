import random
import threading
import time

from config import ButtonConfig
from util.event_bus import EventBus, SensorEvent

def run_button_simulator(
    config: ButtonConfig,
    delay: int,
    event_bus: EventBus,  
    stop_event: threading.Event
) -> None:
    while not stop_event.is_set():
        time.sleep(delay)
        if stop_event.is_set():
            break
        
        if random.uniform(0, 100) < 50:
            event_bus.publish(
                SensorEvent(
                    sensor=config.id,
                    payload={"pressed": True},
                )
            )
        else:
            event_bus.publish(
                SensorEvent(
                    sensor=config.id,
                    payload={"pressed": False},
                )
            )