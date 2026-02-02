import logging
import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from app.app_state import AppState
from components.dl import run_dl
from components.db import run_db
from components.ds1 import run_ds1
from components.dus1 import run_dus1
from components.dpir1 import run_dpir1
from components.dms import run_dms
from config import Config
from util.event_bus import EventBus

logger = logging.getLogger("iot_home")

try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
    GPIO.setmode(GPIO.BCM)
except (ModuleNotFoundError, RuntimeError):
    pass

class SystemManager:
    
    def __init__(self, config: Config):
        self.config = config
        self.threads: List[threading.Thread] = []
        self.stop_event = threading.Event()
        self.event_bus = EventBus()
        self.state = AppState(
            sensors={},
            actuator_registry= ActuatorRegistry(),
        )
        
    def initialize(self) -> None:
        logger.info("Initializing system components...")
        
        self.state.actuator_registry.register("dl")
        self.state.actuator_registry.register("db")
        
        try:
            run_ds1(self.config.ds1_config, self.event_bus, self.threads, self.stop_event)
            run_dus1(self.config.dus1_config, self.event_bus, self.threads, self.stop_event)
            run_dl(self.config.dl_config, self.state.actuator_registry, self.threads, self.stop_event)
            run_db(self.config.db_config, self.state.actuator_registry, self.threads, self.stop_event)
            run_dpir1(self.config.dpir1_config, self.event_bus, self.threads, self.stop_event)
            run_dms(self.config.dms_config, self.event_bus, self.threads, self.stop_event)
            
            logger.info(f"System initialized with {len(self.threads)} components")
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            self.stop_event.set()
            raise
    
    def shutdown(self) -> None:
        logger.info("Shutting down system...")
        self.stop_event.set()
        
        for thread in self.threads:
            thread.join(timeout=2.0)
            if thread.is_alive():
                logger.warning(f"Thread {thread.name} did not stop gracefully")
        
        try:
            GPIO.cleanup()
            logger.debug("GPIO cleaned up")
        except NameError:
            pass
        logger.info("System shutdown complete")
        
    
    def get_status(self) -> dict:
        return {
            "threads_running": sum(1 for t in self.threads if t.is_alive()),
            "total_threads": len(self.threads),
            "actuators": len(self.state.actuator_registry.get_all()),
            "stop_requested": self.stop_event.is_set(),
        }