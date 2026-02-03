import random
import threading
import time

from config import PIRConfig
from util.event_bus import EventBus, SensorEvent

def run_pir_simulator(
    config: PIRConfig,
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
                    payload={"motion": True},
                )
            )
        else:
            event_bus.publish(
                SensorEvent(
                    sensor=config.id,
                    payload={"motion": False},
                )
            )