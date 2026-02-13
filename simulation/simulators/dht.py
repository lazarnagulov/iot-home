import threading
import time
import random

from config import DHTConfig
from util.event_bus import EventBus, SensorEvent

def generate_values(initial_temp = 25, initial_humidity=20):
      temperature = initial_temp
      humidity = initial_humidity
      while True:
            temperature = temperature + random.randint(-1, 1)
            humidity = humidity + random.randint(-1, 1)
            if humidity < 0:
                  humidity = 0
            if humidity > 100:
                  humidity = 100
            yield humidity, temperature

def run_dht_simulator(
    config: DHTConfig,
    delay: float,
    event_bus: EventBus,
    stop_event: threading.Event
) -> None:
    for h, t in generate_values():
        time.sleep(delay) 
        event_bus.publish(
            SensorEvent(
                device_info = config,
                value = { "humidity": h, "temperature": t }
            )
        )
        if stop_event.is_set():
            break
              