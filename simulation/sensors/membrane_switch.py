try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass
import threading
import time
from typing import Optional
from config import MembraneSwitchConfig
from util.event_bus import EventBus, SensorEvent
from util.logger import get_logger

logger = get_logger()

class MembraneSwitch:
    
    KEYMAP  = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"],
    ]
    
    def __init__(self, config: MembraneSwitchConfig, event_bus: EventBus) -> None:
        assert len(config.row_pins) == 4
        assert len(config.col_pins) == 4
        
        self._event_bus = event_bus
        self._row_pins = config.row_pins
        self._col_pins = config.col_pins
        self._config = config
        
        for pin in self._row_pins:
            GPIO.setup(pin, GPIO.OUT)
        
        for pin in self._col_pins:        
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def _read_line(self, line: int, characters: list[str]) -> Optional[str]:
        GPIO.output(line, GPIO.HIGH)

        try:
            for col_pin, ch in zip(self._col_pins, characters):
                if GPIO.input(col_pin):
                    return ch
        finally:
            GPIO.output(line, GPIO.LOW)

        return None

    
    def _publish_key(self, ch: str) -> None:
        logger.debug("[SENSOR: %s] %s", self._config.name, ch)
        self._event_bus.publish(
            SensorEvent(
                device_info=self._config,
                value={"last_key": ch},
            )
        )

    def run(self, stop_event: threading.Event) -> None:
        while not stop_event.is_set():
            for row_pin, keys in zip(self._row_pins, self.KEYMAP):
                if ch := self._read_line(row_pin, keys):
                    self._publish_key(ch)

            time.sleep(0.2)
