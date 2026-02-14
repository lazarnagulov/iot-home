

import threading
from typing import List
from config import GyroscopeConfig
from sensors.gyroscope import Gyroscope
from simulators.gyroscope import run_gyroscope_simulator
from util.logger import get_logger
from util.event_bus import EventBus

logger = get_logger()

def run_gyroscope(config: GyroscopeConfig, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        gyroscope_thread = threading.Thread(target = run_gyroscope_simulator, args=(config, 2, event_bus, stop_event))
        gyroscope_thread.start()
        threads.append(gyroscope_thread)
    else:
        logger.info(f"Starting {config.id} Sensor")
        sensor: Gyroscope = Gyroscope(config, event_bus)
        gyro_thread = threading.Thread(target = sensor.run,  args=(stop_event,))
        gyro_thread.start()
        threads.append(gyro_thread)