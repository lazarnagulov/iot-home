import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from config import RGBDiodeConfig
from actuators.actuator_state import ActuatorState
from actuators.rgb_diode import RGBDiode
from util.event_bus import EventBus
from simulators.actuator import run_actuator_simulator
from util.logger import get_logger


logger = get_logger()

def light_changed(name: str, rgb_light: ActuatorState) -> None:
    logger.info(f"{name} is now { rgb_light }")

def run_rgb_diode(config: RGBDiodeConfig, registry: ActuatorRegistry, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    actuator = registry.get(config.id)
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        diode_thread = threading.Thread(
            target=run_actuator_simulator,
            args=(actuator, config, event_bus, light_changed, stop_event),
            daemon=True
        )
        diode_thread.start()
        threads.append(diode_thread)
    else:
        logger.info(f"Starting {config.id} Sensor")
        driver = RGBDiode(config, actuator)
        diode_thread = threading.Thread(
            target=driver.run,
            args=(stop_event,),
            daemon=True
        )
        diode_thread.start()
        threads.append(diode_thread)