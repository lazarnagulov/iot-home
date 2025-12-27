import threading
from typing import List
from config import DUS1Config
from sensors.ultrasonic import Ultrasonic
from simulators.dus1 import run_dus1_simulator
from util.event_bus import EventBus
from util.logger import get_logger


logger = get_logger()

def run_dus1(config: DUS1Config, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info("Starting DUS1 Simulator")
        dus1_thread = threading.Thread(target = run_dus1_simulator, args=(2, event_bus, stop_event))
        dus1_thread.start()
        threads.append(dus1_thread)
    else:
        logger.info("String DUS1 Sensor")
        sensor: Ultrasonic = Ultrasonic(config, event_bus)
        dus1_thread = threading.Thread(target = sensor.run,  args=(stop_event,))
        dus1_thread.start()
        threads.append(dus1_thread)