import logging
import threading
from typing import List

from actuators.actuator_registry import ActuatorRegistry
from app.app_state import AppState
from simulation.components.diode import run_diode
from simulation.components.buzzer import run_buzzer
from simulation.components.button import run_button
from simulation.components.ultrasonic import run_ultrasonic
from simulation.components.pir import run_pir
from simulation.components.membrane_switch import run_membrane_switch
from config import PiConfig
from util.event_bus import EventBus

logger = logging.getLogger("iot_home")

try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
    GPIO.setmode(GPIO.BCM)
except (ModuleNotFoundError, RuntimeError):
    pass

class SystemManager:
    
    def __init__(self, config: PiConfig):
        self.config = config
        self.threads: List[threading.Thread] = []
        self.stop_event = threading.Event()
        self.event_bus = EventBus()
        self.state = AppState(
            sensors={},
            actuator_registry= ActuatorRegistry(),
        )
        self.sensor_functions = {
            "button": run_button,
            "ultrasonic": run_ultrasonic,
            "pir": run_pir,
            "membrane_switch": run_membrane_switch,
        }
        self.actuator_functions = {
            "diode": run_diode,
            "buzzer": run_buzzer,
        }
        
    def initialize(self) -> None:
        logger.info("Initializing system components...")
        
        for device_id, device_config in self.config.devices.items():
            if self.is_actuator(device_id):
                self.state.actuator_registry.register(device_id)
        
        try:
            for device_id, device_config in self.config.devices.items():
                if self.is_sensor(device_id):
                    run_function = self.sensor_functions[device_id]
                    run_function(device_config, self.event_bus, self.threads, self.stop_event)
                elif self.is_actuator(device_id):
                    run_function = self.actuator_functions[device_id]
                    run_function(device_config, self.state.actuator_registry, self.threads, self.stop_event)
                else:
                    raise ValueError(f"Unknown device type: {device_id}")
            
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
    
    def is_actuator(self, device_id: str) -> bool:
        return device_id in self.actuator_functions.keys()
    
    def is_sensor(self, device_id: str) -> bool:
        return device_id in self.sensor_functions.keys()