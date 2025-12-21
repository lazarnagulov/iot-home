import threading
from typing import List
from config import DS1Config
from simulators.ds1 import run_ds1_simulator
from util.logger import log_message


def button_pressed_callback(event) -> None:
    log_message("Door button pressed! Triggering event...")


def run_ds1(config: DS1Config, threads: List[threading.Thread], stop_event: threading.Event) -> None:
    if config.simulated:
        log_message("String DS1 Simulator")
        ds1_thread = threading.Thread(target = run_ds1_simulator, args=(2, button_pressed_callback, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
    else:
        raise NotImplementedError
