import threading
import time
try:
    from RPi.GPIO import GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass

from typing import Optional
from config import DUS1Config
from util.constants import SPEED_OF_SOUND
from util.event_bus import EventBus, SensorEvent


class Ultrasonic:
        
    def __init__(self, config: DUS1Config, event_bus: EventBus) -> None:
        assert len(config.pins) == 2
        self._trig_pin: int = config.pins[0]
        self._echo_pin: int = config.pins[1]
        self._max_iter: int = config.max_iter
        self._event_bus: EventBus = event_bus
        
        GPIO.setup(self._trig_pin, GPIO.OUT)
        GPIO.setup(self._echo_pin, GPIO.IN)
    
    def get_distance(self) -> Optional[float]:
        GPIO.output(self._trig_pin, False)
        time.sleep(0.2)
        GPIO.output(self._trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self._trig_pin, False)
        pulse_start_time: float = time.time()
        pulse_end_time: float = time.time()
        
        it = 0
        while GPIO.input(self._echo_pin) == 0:
            if it > self._max_iter:
                return None
            pulse_start_time = time.time()
            it += 1
            
        it = 0
        while GPIO.input(self._echo_pin) == 1:
            if it > self._max_iter:
                return None
            pulse_end_time = time.time()
            it += 1
            
        pulse_duration: float = pulse_end_time - pulse_start_time
        return (pulse_duration * SPEED_OF_SOUND) / 2
    
    def run(self, stop_event: threading.Event) -> None:
        while not stop_event.set():
            distance: Optional[float] = self.get_distance()
            self._event_bus.publish(SensorEvent(
                sensor="DUS1",
                payload={ "distance": distance }
            ))
            time.sleep(1)