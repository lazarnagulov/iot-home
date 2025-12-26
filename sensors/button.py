try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass

from config import DS1Config
from util.event_bus import EventBus, SensorEvent


class Button:
    
    def __init__(self, config: DS1Config, event_bus: EventBus) -> None:
        self._pin: int = config.pin
        self._pull_up: bool = config.pull_up
        self._bounce_time: int = config.bounce_time
        self._event_bus: EventBus = event_bus
        self._pressed: bool = False

        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP if self._pull_up else GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            self._pin,
            GPIO.FALLING if self._pull_up else GPIO.RISING,
            callback=lambda _: self._publish_event(),
            bouncetime=self._bounce_time
        )
    
    def _publish_event(self) -> None:
        self._pressed = True
        self._event_bus.publish(SensorEvent("DS1", { "pressed": True }))
    