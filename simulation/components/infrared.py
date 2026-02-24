import multiprocessing
import queue
import threading
from typing import List
from config import IRConfig
from sensors.infrared import Infrared
from simulators.infrared import run_ir_bedroom_simulator
from util.event_bus import EventBus, SensorEvent
from util.logger import get_logger

logger = get_logger()

def run_infrared(
    config: IRConfig,
    event_bus: EventBus,
    threads: List[threading.Thread],
    stop_event: threading.Event
) -> None:
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        ir_thread = threading.Thread(
            target=run_ir_bedroom_simulator,
            args=(config, config.delay, event_bus, stop_event)
        )
        ir_thread.start()
        threads.append(ir_thread)
        return

    logger.info(f"Starting {config.id} Sensor (PROCESS MODE)")

    sensor = Infrared(config)

    ir_queue = multiprocessing.Queue()
    ir_stop = multiprocessing.Event()

    ir_process = multiprocessing.Process(
        target=sensor.run_process,
        args=(ir_queue, ir_stop),
        daemon=True
    )

    ir_process.start()

    def queue_listener():
        while not stop_event.is_set():
            try:
                value = ir_queue.get(timeout=0.5)
                event_bus.publish(
                    SensorEvent(
                        device_info=config,
                        value={"button": value}
                    )
                )
            except queue.Empty:
                continue

        ir_stop.set()
        ir_process.join(timeout=1)

    listener_thread = threading.Thread(target=queue_listener, daemon=True)
    listener_thread.start()

    threads.append(listener_thread)