try:
    from RPi.GPIO import GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass
import queue
import threading
from actuators.actuator_driver import ActuatorDriver
from actuators.actuator_registry import Actuator
from actuators.actuator_state import ActuatorState, OnOffState
from config import DLConfig


class DL(ActuatorDriver):
    
    def __init__(self, config: DLConfig, actuator: Actuator) -> None:
        self._pin: int = config.pin
        self._actuator: Actuator = actuator
        GPIO.setup(self._pin, GPIO.OUT)

    def apply(self, state: ActuatorState) -> None:
        if not isinstance(state, OnOffState):
            raise TypeError("DL only supports OnOffState")

        state.validate()

        GPIO.output(
            self._pin,
            GPIO.HIGH if state.value else GPIO.LOW
        )
    
    def cleanup(self) -> None:
        pass
    
    def run(self, stop_event: threading.Event) -> None:
        while not stop_event.is_set():
            try:
                state = self._actuator.commands.get(timeout=0.5)
            except queue.Empty:
                continue

        self.apply(state)
