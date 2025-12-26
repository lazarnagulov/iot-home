import queue
import threading
from typing import List

from actuators.actuator_driver import ActuatorDriver
from actuators.actuator_registry import Actuator, ActuatorRegistry
from actuators.dl import DL
from config import DLConfig
from simulators.actuator import run_actuator_simulator
from util.logger import get_logger


logger = get_logger()

def run_actuator_worker(
    actuator: Actuator,
    driver: ActuatorDriver,
    stop_event: threading.Event
) -> None:
    while not stop_event.is_set():
        try:
            state = actuator.commands.get(timeout=0.5)
        except queue.Empty:
            continue

        driver.apply(state)

def door_light_changed(name: str, is_on: bool) -> None:
    logger.info(f"{name} is now {'ON' if is_on else 'OFF'}")

def run_dl(config: DLConfig, registry: ActuatorRegistry,  threads: List[threading.Thread], stop_event: threading.Event) -> None:
    actuator = registry.get("dl")
    if config.simulated:
        logger.info("Starting DL Simulator")
        dl_thread = threading.Thread(
            target=run_actuator_simulator,
            args=(actuator, door_light_changed, stop_event),
            daemon=True
        )
        dl_thread.start()
        threads.append(dl_thread)
    else:
        logger.info("Starting DL")
        dl_thread = threading.Thread(
            target=run_actuator_worker,
            args=(actuator, DL(config), stop_event),
            daemon=True
        )
        dl_thread.start()
        threads.append(dl_thread)
    