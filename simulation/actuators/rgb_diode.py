try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass
import queue
import threading
from actuators.actuator_driver import ActuatorDriver
from actuators.actuator_state import ActuatorState, RGBState
from config import RGBDiodeConfig
from actuators.actuator_registry import Actuator


class RGBDiode(ActuatorDriver):
    
    def __init__(self, config: RGBDiodeConfig, actuator: Actuator) -> None:
        self._red_pin = config.red_pin
        self._green_pin = config.green_pin
        self._blue_pin = config.blue_pin
        self._actuator = actuator
        
        GPIO.setup(self._red_pin,  GPIO.OUT)
        GPIO.setup(self._green_pin, GPIO.OUT)
        GPIO.setup(self._blue_pin, GPIO.OUT)
    
    def apply(self, state: ActuatorState) -> None: 
        if not isinstance(state, RGBState):
            raise TypeError("RGB Diode only supports RGBState")

        state.validate()
        
        GPIO.output(self._red_pin, GPIO.LOW if state.r == 0 else GPIO.HIGH)
        GPIO.output(self._green_pin, GPIO.LOW if state.g == 0 else GPIO.HIGH)
        GPIO.output(self._blue_pin, GPIO.LOW if state.b == 0 else GPIO.HIGH)
        
    def cleanup(self) -> None:
        for pin in (self._red_pin, self._green_pin, self._blue_pin):
            GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup(pin)

    
    def run(self, stop_event: threading.Event) -> None:
        try:
            while not stop_event.is_set():
                try:
                    state = self._actuator.commands.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                self.apply(state)
        finally:
            self.cleanup()