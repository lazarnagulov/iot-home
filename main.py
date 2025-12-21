
import logging
import threading
import time
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from app.app_state import AppState
from app.cli.console import run_actuator_cli
from app.tui.iot_home import IotHomeApp
from components.dl import run_dl
from components.ds1 import run_ds1
from components.dus1 import run_dus1
from config import Config, load_config
from util.logger import setup_logger

setup_logger(mode="cli")

logger = logging.getLogger("iot_home")

try:
    import RPi.GPIO as GPIO # ty: ignore[unresolved-import]
    GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError:
    pass


def main() -> None:
    logger.info('Starting app...')
    config: Config = load_config()
    threads: List[threading.Thread] = []
    stop_event: threading.Event = threading.Event()
    
    registry: ActuatorRegistry = ActuatorRegistry()
    registry.register("dl")

    console_thread: threading.Thread = threading.Thread(
        target=run_actuator_cli,
        args=(registry, stop_event),
        daemon=True
    )
    console_thread.start()
    threads.append(console_thread)

    try:
        run_ds1(config.ds1_config, threads, stop_event)
        run_dus1(config.dus1_config, threads, stop_event)
        
        run_dl(config.dl_config, registry, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info('Stopping app')
        for _ in threads:
            stop_event.set()

        try:
            GPIO.cleanup()
        except NameError:
            pass
            

# if __name__ == "__main__":
#     main()
    
if __name__ == "__main__":
    state = AppState()
    registry: ActuatorRegistry = ActuatorRegistry()
    registry.register("dl")
    
    state.sensors = {
        "DS1": {"pressed": True},
        "DHT1": {"temp": 23.4, "hum": 40},
        "PIR1": {"motion": False},
    }
    state.actuator_registry = registry
    app = IotHomeApp(state)
    app.run()