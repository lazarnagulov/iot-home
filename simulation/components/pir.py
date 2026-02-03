import threading
from typing import List
from config import PIRConfig
from simulation.simulators.pir import run_pir_simulator
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()

def run_pir(config: PIRConfig, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        pir_thread = threading.Thread(target = run_pir_simulator, args=(config, 2, event_bus, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        raise NotImplementedError
