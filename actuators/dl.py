try:
    from RPi.GPIO import GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass
from actuators.actuator_driver import ActuatorDriver
from actuators.actuator_state import ActuatorState, OnOffState
from config import DLConfig


class DL(ActuatorDriver):
    
    def __init__(self, config: DLConfig) -> None:
        self._pin = config.pin
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