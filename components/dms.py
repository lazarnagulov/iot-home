import threading
from typing import List
from config import DMSConfig
from simulators.dms import run_dms_simulator
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()


def run_dms(config: DMSConfig, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info("Starting DMS Simulator")
        dms_thread = threading.Thread(target = run_dms_simulator, args=(4, event_bus, stop_event))
        dms_thread.start()
        threads.append(dms_thread)
    else:
        raise NotImplementedError
