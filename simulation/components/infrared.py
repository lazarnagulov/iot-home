import threading
from typing import List
from config import IRConfig
from sensors.infrared import Infrared
from simulators.infrared import run_ir_bedroom_simulator
from util.event_bus import EventBus
from util.logger import get_logger

logger = get_logger()

def run_infrared(
    config: IRConfig,
    event_bus: EventBus,
    threads: List[threading.Thread],
    stop_event: threading.Event,
    pause_event: threading.Event
) -> None:
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        ir_thread = threading.Thread(
            target=run_ir_bedroom_simulator,
            args=(config, config.delay, event_bus, stop_event, pause_event)
        )
        ir_thread.start()
        threads.append(ir_thread)
    else:
        logger.info(f"Starting {config.id} Sensor")
        sensor: Infrared = Infrared(config, event_bus)
        ir_thread = threading.Thread(target = sensor.run,  args=(stop_event,))
        ir_thread.start()
        threads.append(ir_thread)
