import threading
from typing import List

from actuators.lcd import LCD
from config import LCDConfig
from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import ActuatorState
from simulators.actuator import run_actuator_simulator
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()

def lcd_changed(name: str, display_state: ActuatorState) -> None:
    logger.info(f"{name} now displays { display_state }")

def run_lcd(config: LCDConfig, registry: ActuatorRegistry, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    actuator = registry.get(config.id)
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        lcd_thread = threading.Thread(
            target=run_actuator_simulator,
            args=(actuator, config, event_bus, lcd_changed, stop_event),
            daemon=True
        )
        lcd_thread.start()
        threads.append(lcd_thread)
    else:
        logger.info(f"Starting {config.id} Actuator")
        driver = LCD(config, actuator)
        lcd_thread = threading.Thread(
            target=driver.run,
            args=(stop_event,),
            daemon=True
        )
        lcd_thread.start()
        threads.append(lcd_thread)