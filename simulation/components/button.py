import threading
from typing import List
from config import ButtonConfig
from sensors.button import Button
from simulators.button import run_button_simulator
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()

def run_button(config: ButtonConfig, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        button_thread = threading.Thread(target = run_button_simulator, args=(config, 2, event_bus, stop_event))
        button_thread.start()
        threads.append(button_thread)
    else:
        logger.info(f"Starting {config.id} Sensor")
        Button(config, event_bus)
