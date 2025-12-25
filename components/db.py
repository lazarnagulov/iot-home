import logging
import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from config import DBConfig
from simulators.actuator import run_actuator_simulator
from util.logger import get_logger

logger = get_logger()

def door_buzzer_changed(name: str, is_on: bool) -> None:
    logger.info(f"{name} is now {'ON' if is_on else 'OFF'}")

def run_db(config: DBConfig, registry: ActuatorRegistry,  threads: List[threading.Thread], stop_event: threading.Event) -> None:
    actuator = registry.get("db")
    if config.simulated:
        logger.info("Starting DB Simulator")
        db_thread = threading.Thread(
            target=run_actuator_simulator,
            args=(actuator, door_buzzer_changed, stop_event),
            daemon=True
        )
        db_thread.start()
        threads.append(db_thread)
    else:
        raise NotImplementedError
    