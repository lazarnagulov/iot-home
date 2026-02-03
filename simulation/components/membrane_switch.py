import threading
from typing import List
from config import MembraneSwitchConfig
from simulation.simulators.membrane_switch import run_membrane_switch_simulator
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()


def run_membrane_switch(config: MembraneSwitchConfig, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        ms_thread = threading.Thread(target = run_membrane_switch_simulator, args=(config, 4, event_bus, stop_event))
        ms_thread.start()
        threads.append(ms_thread)
    else:
        raise NotImplementedError
