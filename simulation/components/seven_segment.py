

import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from actuators.seven_segment import SevenSegment
from config import SevenSegmentConfig
from actuators.actuator_state import ActuatorState, DisplayState
from simulators.actuator import run_actuator_simulator
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()

def seven_segment_changed(name: str, display_state: ActuatorState) -> None:
    if not isinstance(display_state, DisplayState):
        raise TypeError("SevenSegment only supports DisplayState")
    
    if display_state.text == "reset":
        logger.info(f"Reseting {name} to 0000")
    elif display_state.text == "0000":
        logger.info(f"{name} now displays { display_state } and blinks")
    else:
        logger.info(f"{name} now displays { display_state }")

def run_seven_segment_display(
    config: SevenSegmentConfig, 
    registry: ActuatorRegistry, 
    event_bus: EventBus, 
    threads: List[threading.Thread], 
    stop_event: threading.Event
) -> None:
    actuator = registry.get(config.id)
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        ssd_thread = threading.Thread(
            target=run_actuator_simulator,
            args=(actuator, config, event_bus, seven_segment_changed, stop_event),
            daemon=True
        )
        ssd_thread.start()
        threads.append(ssd_thread)
    else:
        logger.info(f"Starting {config.id} Actuator")
        driver = SevenSegment(config, actuator)
        ss_thread = threading.Thread(
            target=driver.run,
            args=(stop_event,),
            daemon=True
        )
        ss_thread.start()
        threads.append(ss_thread)