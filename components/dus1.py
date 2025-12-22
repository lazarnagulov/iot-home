import logging
import threading
from typing import List
from config import DUS1Config
from simulators.dus1 import run_dus1_simulator
from util.event_bus import EventBus

logger = logging.getLogger("iot_home")


def run_dus1(config: DUS1Config, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info("Starting DUS1 Simulator")
        dus1_thread = threading.Thread(target = run_dus1_simulator, args=(2, event_bus, stop_event))
        dus1_thread.start()
        threads.append(dus1_thread)
    else:
        raise NotImplementedError
