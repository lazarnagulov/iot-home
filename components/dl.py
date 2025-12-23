import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from config import DLConfig
from simulators.actuator import run_actuator_simulator
from util.logger import log_message


def door_light_changed(name: str, is_on: bool) -> None:
    log_message(f"{name} is now {'ON' if is_on else 'OFF'}")

def run_dl(config: DLConfig, registry: ActuatorRegistry,  threads: List[threading.Thread], stop_event: threading.Event) -> None:
    actuator = registry.get("dl")
    if config.simulated:
        log_message("Starting DL Simulator")
        dl_thread = threading.Thread(
            target=run_actuator_simulator,
            args=(actuator, door_light_changed, stop_event),
            daemon=True
        )
        dl_thread.start()
        threads.append(dl_thread)
    else:
        raise NotImplementedError
    