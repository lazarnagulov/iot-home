import threading
from typing import List

from actuators.lcd import LCD
from config import LCDConfig
from simulation.actuators.actuator_registry import ActuatorRegistry
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()

def run_lcd(config: LCDConfig, registry: ActuatorRegistry, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    actuator = registry.get(config.id)
    if config.simulated:
        raise NotImplementedError
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