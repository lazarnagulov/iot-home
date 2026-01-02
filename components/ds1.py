import threading
from typing import List
from config import DS1Config
from sensors.button import Button
from simulators.ds1 import run_ds1_simulator
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()

def run_ds1(config: DS1Config, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info("String DS1 Simulator")
        ds1_thread = threading.Thread(target = run_ds1_simulator, args=(2, event_bus, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
    else:
        logger.info("String DS1 Sensor")
        Button(config, event_bus)
