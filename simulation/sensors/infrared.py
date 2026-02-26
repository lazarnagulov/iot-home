try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass
from multiprocessing.queues import Queue
from multiprocessing.synchronize import Event
import time

class Infrared:

    BUTTON_MAP = {
        "0x2807fb14e": "UP",
        "0x2807fd42b": "DOWN",
        "0x2807f916e": "LEFT",
        "0x2807fe11e": "RIGHT",
        "0x2807f817e": "OK",

        "0x2807fb44b": "1",
        "0x2807fcc33": "2",
        "0x2807fd827": "3",
        "0x2807f9867": "4",
        "0x2807f8c73": "5",
        "0x2807fbd42": "6",
        "0x2807f8877": "7",
        "0x2807f9c63": "8",
        "0x2807fad52": "9",
        "0x2807fa15e": "*",
        "0x2807fa55a": "0",
        "0x2807fa956": "#", 
    }

    def __init__(self, config):
        self._config = config
        self._pin = config.pin

    def run_process(self, queue: Queue, stop_event: Event):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN)

        while not stop_event.is_set():
            value = self._get_binary()
            if value:
                hex_val = self._convert_hex(value)
                button = self.BUTTON_MAP.get(hex_val)
                if button:
                    queue.put(button)

        GPIO.cleanup(self._pin)

    def _get_binary(self):
        num1s = 0
        binary = 1
        command = []

        previous_value = GPIO.input(self._pin)
        value = previous_value

        while value:
            value = GPIO.input(self._pin)

        start_time = time.monotonic_ns()

        while True:
            if previous_value != value:
                now = time.monotonic_ns()
                pulse_time = (now - start_time) // 1000
                start_time = now
                command.append((previous_value, pulse_time))

            if value:
                num1s += 1
            else:
                num1s = 0

            if num1s > 10000:
                break

            previous_value = value
            value = GPIO.input(self._pin)

        for typ, tme in command:
            if typ == 1:
                if tme > 1300:
                    binary = binary * 10 + 1
                else:
                    binary *= 10

        if len(str(binary)) > 34:
            binary = int(str(binary)[:34])

        return binary

    def _convert_hex(self, binary_value):
        return hex(int(str(binary_value), 2))