try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass

from config import PIRConfig
from util.event_bus import EventBus, SensorEvent


class PIR:
    
    def __init__(self, config: PIRConfig, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._config = config
        self._pin = config.pin
        
        GPIO.setup(self._pin, GPIO.IN)    
    
    def run(self) -> None:
        GPIO.add_event_detect(
            self._pin,
            GPIO.BOTH,
            callback=self._handle_motion,
            bouncetime=200
        )

    def _handle_motion(self, _channel) -> None:
        if GPIO.input(self._pin):
            self._event_bus.publish(SensorEvent(device_info=self._config, value={"motion": True}))
        else:
            self._event_bus.publish(SensorEvent(device_info=self._config, value={"motion": False}))