from RPi.GPIO import GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
from config import DLConfig


class DL:

    def __init__(self, config: DLConfig) -> None:
        self._pin = config.pin
        
        GPIO.setup(self._pin,GPIO.OUT)

    def turn_on(self) -> None:
        GPIO.output(self._pin, GPIO.HIGH)

    def turn_off(self) -> None:
        GPIO.output(self._pin, GPIO.LOW)
        
    