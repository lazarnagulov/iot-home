import logging
import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from components.dl import run_dl
from components.ds1 import run_ds1
from components.dus1 import run_dus1
from config import Config

logger = logging.getLogger("iot_home")

try:
    import RPi.GPIO as GPIO # ty: ignore[unresolved-import]
    GPIO.setmode(GPIO.BCM)
except (ModuleNotFoundError, RuntimeError):
    pass

class SystemManager:
    
    def __init__(self, config: Config):
        self.config = config
        self.threads: List[threading.Thread] = []
        self.stop_event = threading.Event()
        self.registry = ActuatorRegistry()
        
    def initialize(self) -> None:
        logger.info("Initializing system components...")
        
        self.registry.register("dl")
        
        try:
            run_ds1(self.config.ds1_config, self.threads, self.stop_event)
            run_dus1(self.config.dus1_config, self.threads, self.stop_event)
            run_dl(self.config.dl_config, self.registry, self.threads, self.stop_event)
            
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
            "actuators": len(self.registry.get_all()),
            "stop_requested": self.stop_event.is_set(),
        }