import logging
import threading
from typing import List
from config import DPIR1Config
from simulators.dpir1 import run_dpir1_simulator
from util.event_bus import EventBus

logger = logging.getLogger("iot_home")

def run_dpir1(config: DPIR1Config, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info("String DPIR1 Simulator")
        dpir1_thread = threading.Thread(target = run_dpir1_simulator, args=(2, event_bus, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
    else:
        raise NotImplementedError
