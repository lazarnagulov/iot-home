

import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from actuators.seven_segment import SevenSegment
from config import SevenSegmentConfig
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()

def run_seven_segment_display(
    config: SevenSegmentConfig, 
    registry: ActuatorRegistry, 
    event_bus: EventBus, 
    threads: List[threading.Thread], 
    stop_event: threading.Event
) -> None:
    actuator = registry.get(config.id)
    if config.simulated:
        raise NotImplementedError
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