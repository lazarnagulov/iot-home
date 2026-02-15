try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except ModuleNotFoundError:
    pass
import datetime
import threading
import time
from config import IRConfig
from util.logger import get_logger
from util.event_bus import EventBus, SensorEvent

logger = get_logger()

class Infrared:
    
    BUTTONS       = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897, 0x300ff02fd, 0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5, 0x300ff52ad]  # HEX code list
    BUTTONS_NAMES = ["LEFT",   "RIGHT",      "UP",       "DOWN",       "2",          "3",          "1",        "OK",        "4",         "5",         "6",         "7",         "8",          "9",        "*",         "0",        "#"]  # String list in same order as HEX list

        
    def __init__(self, config: IRConfig, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._config = config
        self._pin = config.pin
        
        GPIO.setup(self._pin, GPIO.IN)
    
    def _get_binary(self):
        num1s = 0
        binary = 1
        command = []
        previous_value = 0
        value = GPIO.input(self._pin) 

        while value:
            time.sleep(0.0001) 
            value = GPIO.input(self._pin)
            
        start_time = datetime.datetime.now()
        
        while True:
            if previous_value != value:
                now = datetime.datetime.now()
                pulse_time = now - start_time
                start_time = now
                command.append((previous_value, pulse_time.microseconds)) 
                
            if value:
                num1s += 1
            else:
                num1s = 0
            
            if num1s > 10000:
                break
                
            previous_value = value
            value = GPIO.input(self._pin)
            
        for (typ, tme) in command:
            if typ == 1:
                if tme > 1000:
                    binary = binary *10 +1
                else:
                    binary *= 10
                
        if len(str(binary)) > 34:
            binary = int(str(binary)[:34])
            
        return binary
    
    def _convert_hex(self, binary_value):
        tmpB2 = int(str(binary_value),2)
        return hex(tmpB2)
    
    def run(self, stop_event: threading.Event) -> None:
        while not stop_event.is_set():
            in_data = self._convert_hex(self._get_binary())
            for button in range(len(self.BUTTONS)):
                if hex(self.BUTTONS[button]) == in_data:
                    button_name = self.BUTTONS[button]
                    logger.debug(f"{self._config.name}: {button_name}")
                    self._event_bus.publish(SensorEvent(device_info=self._config, values = { "button" : button_name }))