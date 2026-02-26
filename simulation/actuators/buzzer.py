try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass
import queue
import threading
import time

from config import BuzzerConfig
from actuators.actuator_driver import ActuatorDriver
from actuators.actuator_registry import Actuator
from actuators.actuator_state import ActuatorState, OnOffState


class Buzzer(ActuatorDriver):
    
    def __init__(self, config: BuzzerConfig, actuator: Actuator) -> None:
        self._actuator = actuator
        self._pin = config.pin
        self._pitch = config.pitch
        self._alternate_pitch = config.alternate_pitch
        self._duty_cycle = config.duty_cycle
        self._alarm_active = False
        self._alarm_thread = None
        self._pulse_duration = config.pulse_duration
        self._pause_duration = config.pause_duration
        self._is_active = config.is_active
        
        if self._is_active:
            GPIO.setup(self._pin, GPIO.OUT)
        else:
            GPIO.setup(self._pin, GPIO.OUT)
            self._buzz = GPIO.PWM(self._pin, 440)

    def apply(self, state: ActuatorState) -> None:
        if not isinstance(state, OnOffState):
            raise TypeError(f"Buzzer only supports OnOffState")

        state.validate()

        if state.value:
            if not self._alarm_active:
                self._alarm_active = True
                self._start_alarm_thread()
        else:
            self._alarm_active = False
            self._stop_alarm()
        
    def cleanup(self) -> None:
        self._alarm_active = False
        GPIO.output(self._pin, GPIO.LOW)
        GPIO.cleanup(self._pin)  
        
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

    def _pulse_block(self, frequency: int, duration: float) -> None:
        if frequency <= 0:
            return
        period = 1.0 / frequency
        half_period = period / 2.0
        cycles = int(duration * frequency)

        for _ in range(cycles):
            if not self._alarm_active:
                break
            GPIO.output(self._pin, GPIO.HIGH)
            time.sleep(half_period)
            GPIO.output(self._pin, GPIO.LOW)
            time.sleep(half_period)
            
    def _run_alarm(self) -> None:
        while self._alarm_active:
            if self._is_active:
                self._pulse_block(self._pitch, self._pulse_duration)
                if self._alternate_pitch:
                    self._pulse_block(self._alternate_pitch, self._pulse_duration)
            else:
                self._buzz.ChangeFrequency(self._pitch)
                self._buzz.start(self._duty_cycle)
                time.sleep(self._pulse_duration)

                if self._alternate_pitch:
                    self._buzz.ChangeFrequency(self._alternate_pitch)
                    time.sleep(self._pulse_duration)

                self._buzz.stop()

            time.sleep(self._pause_duration)

    def _stop_alarm(self) -> None:
        if not self._is_active:
            self._buzz.stop()
        GPIO.output(self._pin, GPIO.LOW)

    def _start_alarm_thread(self) -> None:
        self._alarm_thread = threading.Thread(
            target=self._run_alarm,
            daemon=True
        )
        self._alarm_thread.start()
