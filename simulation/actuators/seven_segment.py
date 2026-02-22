try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass
import queue
import threading
import time

from actuators.actuator_driver import ActuatorDriver
from actuators.actuator_registry import Actuator
from actuators.actuator_state import ActuatorState, DisplayState
from config import SevenSegmentConfig


class SevenSegment(ActuatorDriver):

    NUM = {
        ' ':(0,0,0,0,0,0,0),
        '0':(1,1,1,1,1,1,0),
        '1':(0,1,1,0,0,0,0),
        '2':(1,1,0,1,1,0,1),
        '3':(1,1,1,1,0,0,1),
        '4':(0,1,1,0,0,1,1),
        '5':(1,0,1,1,0,1,1),
        '6':(1,0,1,1,1,1,1),
        '7':(1,1,1,0,0,0,0),
        '8':(1,1,1,1,1,1,1),
        '9':(1,1,1,1,0,1,1)
    }
    
    def __init__(self, config: SevenSegmentConfig, actuator: Actuator) -> None:
        self._config = config
        self._actuator = actuator
        
        for segment in self._config.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
    
        for digit in self._config.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)
    
    
    def apply(self, state: ActuatorState) -> None:
        if not isinstance(state, DisplayState):
            raise TypeError("SevenSegment only supports DisplayState")

        state.validate()

        self._current_text = state.text.ljust(self._config.num_digits)[:self._config.num_digits]

    def cleanup(self) -> None:
        for pin in self._config.segments:
            GPIO.output(pin, 0)
        for pin in self._config.digits:
            GPIO.output(pin, 1)
        GPIO.cleanup(self._config.segments + self._config.digits)
    
    def run(self, stop_event: threading.Event) -> None: 
        try:
            while not stop_event.is_set():
                try:
                    state = self._actuator.commands.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                self.apply(state)
                
                for i, digit_pin in enumerate(self._config.digits):
                    GPIO.output(digit_pin, 0)
                    
                    char = self._current_text[i] if i < len(self._current_text) else ' '
                    segments_state = self.NUM.get(char, self.NUM[' '])
                    for seg_pin, on in zip(self._config.segments, segments_state):
                        GPIO.output(seg_pin, on)
                    
                    time.sleep(self._config.refresh_interval / len(self._config.digits))
                    GPIO.output(digit_pin, 1)
        finally:
            self.cleanup()