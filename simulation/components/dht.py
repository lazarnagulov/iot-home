import threading
from typing import List
from config import DHTConfig
from simulation.sensors.dht import DHT
from simulators.dht import run_dht_simulator
from util.event_bus import EventBus
from util.logger import get_logger


logger = get_logger()

def run_dht(config: DHTConfig, event_bus: EventBus, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        logger.info(f"Starting {config.id} Simulator")
        pir_thread = threading.Thread(target = run_dht_simulator, args=(config, config.delay, event_bus, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        logger.info(f"Starting {config.id} Sensor")
        sensor: DHT = DHT(config)
        dht_thread = threading.Thread(target = sensor.run,  args=(stop_event,))
        dht_thread.start()
        threads.append(dht_thread)