import random
import threading
import time

from util.event_bus import EventBus, SensorEvent

def run_ds1_simulator(
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
                    sensor="DS1",
                    payload={"pressed": True},
                )
            )
        else:
            event_bus.publish(
                SensorEvent(
                    sensor="DS1",
                    payload={"pressed": False},
                )
            )