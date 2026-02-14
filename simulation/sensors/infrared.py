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
    
    BUTTONS = {
        0x300FF22DD: "LEFT",
        0x300FFC23D: "RIGHT",
        0x300FF629D: "UP",
        0x300FFA857: "DOWN",
        0x300FF9867: "2",
        0x300FFB04F: "3",
        0x300FF6897: "1",
        0x300FF02FD: "OK",
        0x300FF30CF: "4",
        0x300FF18E7: "5",
        0x300FF7A85: "6",
        0x300FF10EF: "7",
        0x300FF38C7: "8",
        0x300FF5AA5: "9",
        0x300FF42BD: "*",
        0x300FF4AB5: "0",
        0x300FF52AD: "#",
    }
        
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
        return int(str(binary_value), 2)
    
    def run(self, stop_event: threading.Event) -> None:
        while not stop_event.is_set():
            binary = self._get_binary()
            command = self._convert_hex(binary)

            button_name = self.BUTTONS.get(command)
            if button_name:
                logger.debug(f"{self._config.name}: {button_name}")
                self._event_bus.publish(SensorEvent(device_info=self._config, value= { "button" : button_name }))
        