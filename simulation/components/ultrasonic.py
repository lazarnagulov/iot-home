import threading
from typing import List
from config import UltrasonicConfig
from sensors.ultrasonic import Ultrasonic
from simulation.simulators.ultrasonic import run_ultrasonic_simulator
from util.event_bus import EventBus
from util.logger import get_logger


logger = get_logger()

def run_ultrasonic(config: UltrasonicConfig, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        us_thread = threading.Thread(target = run_ultrasonic_simulator, args=(config, 2, event_bus, stop_event))
        us_thread.start()
        threads.append(us_thread)
    else:
        logger.info(f"Starting {config.id} Sensor")
        sensor: Ultrasonic = Ultrasonic(config, event_bus)
        us_thread = threading.Thread(target = sensor.run,  args=(stop_event,))
        us_thread.start()
        threads.append(us_thread)