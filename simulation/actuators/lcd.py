import queue
import threading
from config import LCDConfig
from actuators.actuator_driver import ActuatorDriver
from actuators.actuator_registry import Actuator
from actuators.actuator_state import ActuatorState
from actuators.actuator_state import DisplayState
from util.logger import get_logger

logger = get_logger()

try:
    from PCF8574 import PCF8574_GPIO  # pyright: ignore[reportMissingImports] # ty: ignore[unresolved-import]
    from actuators.LCD1602.Adafruit_LCD1602 import Adafruit_CharLCD
except ModuleNotFoundError:
    pass


class LCD(ActuatorDriver):

    def __init__(self, config: LCDConfig, actuator: Actuator) -> None:
        self._config = config
        self._actuator = actuator
        self._lock = threading.Lock()
        self._current_text = [""] * self._config.rows

        try:
            self._mcp = PCF8574_GPIO(config.i2c_address)
        except Exception:
            try:
                self._mcp = PCF8574_GPIO(config.fallback_address)
            except Exception:
                logger.error("I2C Address Error!")
                raise

        self._lcd = Adafruit_CharLCD(
            pin_rs=0,
            pin_e=2,
            pins_db=[4, 5, 6, 7],
            GPIO=self._mcp
        )

        if config.backlight_enabled:
            self._mcp.output(config.backlight_pin, 1)

        self._lcd.begin(config.columns, config.rows)

    def apply(self, state: ActuatorState) -> None:
        if not isinstance(state, DisplayState):
            raise TypeError("LCD only supports DisplayState")

        state.validate()

        parts = state.text.split("\n", self._config.rows - 1)
        with self._lock:
            for i in range(self._config.rows):
                line = parts[i] if i < len(parts) else ""
                self._current_text[i] = line[:self._config.columns].ljust(self._config.columns)

        with self._lock:
            self._lcd.clear()
            for row, line in enumerate(self._current_text):
                self._lcd.setCursor(0, row)
                self._lcd.message(line)

    def cleanup(self) -> None:
        self._lcd.clear()

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