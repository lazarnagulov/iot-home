import threading
from typing import List
from config import DUS1Config
from simulators.dus1 import run_dus1_simulator
from util.logger import log_message

def distance_callback(distance: float) -> None:
    log_message(f"DUS1 Sensor: Distance measured at {distance:.2f} cm. Monitoring continues...")


def run_dus1(config: DUS1Config, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        log_message("Starting DUS1 Simulator")
        dus1_thread = threading.Thread(target = run_dus1_simulator, args=(2, distance_callback, stop_event))
        dus1_thread.start()
        threads.append(dus1_thread)
    else:
        raise NotImplementedError
