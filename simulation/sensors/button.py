try:
    import RPi.GPIO as GPIO  # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass

from config import ButtonConfig
from util.event_bus import EventBus, SensorEvent


class Button:

    def __init__(self, config: ButtonConfig, event_bus: EventBus) -> None:
        self._pin: int = config.pin
        self._pull_up: bool = config.pull_up
        self._bounce_time: int = config.bounce_time
        self._event_bus: EventBus = event_bus
        self._config: ButtonConfig = config

        GPIO.setup(
            self._pin,
            GPIO.IN,
            pull_up_down=GPIO.PUD_UP if self._pull_up else GPIO.PUD_DOWN
        )

        GPIO.add_event_detect(
            self._pin,
            GPIO.BOTH,
            callback=self._handle_change,
            bouncetime=self._bounce_time
        )

    def _handle_change(self, channel: int) -> None:
        pin_state = GPIO.input(self._pin)

        if self._pull_up:
            pressed = pin_state == GPIO.LOW
        else:
            pressed = pin_state == GPIO.HIGH

        self._event_bus.publish(
            SensorEvent(self._config, {"pressed": pressed})
        )