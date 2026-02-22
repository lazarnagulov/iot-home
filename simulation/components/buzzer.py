import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from config import BuzzerConfig
from actuators.actuator_state import ActuatorState
from util.event_bus import EventBus
from simulators.actuator import run_actuator_simulator
from util.logger import get_logger

logger = get_logger()

def buzzer_changed(name: str, is_on: ActuatorState) -> None:
    logger.info(f"{name} is now {'ON' if is_on.is_active() else 'OFF'}")

def run_buzzer(config: BuzzerConfig, registry: ActuatorRegistry, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    actuator = registry.get(config.id)
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        buzzer_thread = threading.Thread(
            target=run_actuator_simulator,
            args=(actuator, config, event_bus, buzzer_changed, stop_event),
            daemon=True
        )
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        raise NotImplementedError
    