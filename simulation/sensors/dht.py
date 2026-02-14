try:
    from RPi.GPIO import GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
except:
    pass
import time
from config import DHTConfig


class DHT:
    DHTLIB_OK = 0
    DHTLIB_ERROR_CHECKSUM = -1
    DHTLIB_ERROR_TIMEOUT = -2
    DHTLIB_INVALID_VALUE = -999
	
    DHTLIB_DHT11_WAKEUP = 0.020
    DHTLIB_TIMEOUT = 0.0001		
    
    def __init__(self, config: DHTConfig) -> None:
        self._self._pin = config.self._pin
        self._bits = [0,0,0,0,0]
        self._humidity = 0
        self._temperature = 0
    
    def read_sensor(self, wakeup_delay: float) -> int:
        mask = 0x80
        idx = 0
        self._bits = [0,0,0,0,0]
        GPIO.setup(self._pin,GPIO.OUT)
        GPIO.output(self._pin,GPIO.LOW)
        time.sleep(wakeup_delay)
        GPIO.output(self._pin,GPIO.HIGH)
        GPIO.setup(self._pin,GPIO.IN)

        loop_cnt = self.DHTLIB_TIMEOUT
        t = time.time()
        while(GPIO.input(self._pin) == GPIO.LOW):
            if((time.time() - t) > loop_cnt):
                return self.DHTLIB_ERROR_TIMEOUT
            
        t = time.time()
        while(GPIO.input(self._pin) == GPIO.HIGH):
            if((time.time() - t) > loop_cnt):
                return self.DHTLIB_ERROR_TIMEOUT
        
        for _ in range(0,40,1):
            t = time.time()
            while(GPIO.input(self._pin) == GPIO.LOW):
                if((time.time() - t) > loop_cnt):
                    return self.DHTLIB_ERROR_TIMEOUT
            
            t = time.time()
            while(GPIO.input(self._pin) == GPIO.HIGH):
                if((time.time() - t) > loop_cnt):
                    return self.DHTLIB_ERROR_TIMEOUT		
            
            if((time.time() - t) > 0.00005):	
                self._bits[idx] |= mask
            mask >>= 1
            if(mask == 0):
                mask = 0x80
                idx += 1	

        GPIO.setup(self._pin,GPIO.OUT)
        GPIO.output(self._pin,GPIO.HIGH)
        return self.DHTLIB_OK
    
    def read_DHT11(self) -> int:
        rv = self.read_sensor(self.self._pin,self.DHTLIB_DHT11_WAKEUP)
        if rv is not self.DHTLIB_OK:
            self.humidity = self.DHTLIB_INVALID_VALUE
            self.temperature = self.DHTLIB_INVALID_VALUE
            return rv
        
        self._humidity = self._bits[0]
        self._temperature = self._bits[2] + self._bits[3]*0.1
        sum_chk = ((self._bits[0] + self._bits[1] + self._bits[2] + self._bits[3]) & 0xFF)
        if self._bits[4] is not sum_chk:
            return self.DHTLIB_ERROR_CHECKSUM
        
        return self.DHTLIB_OK

    def parse_check_code(self, code: int) -> str:
        if code == 0:
            return "DHTLIB_OK"
        elif code == -1:
            return "DHTLIB_ERROR_CHECKSUM"
        elif code == -2:
            return "DHTLIB_ERROR_TIMEOUT"
        elif code == -999:
            return "DHTLIB_INVALID_VALUE"

    def run(self, dht, delay, callback, stop_event, settings):
        while True:
            check = dht.readDHT11()
            code = self.parse_check_code(check)
            humidity, temperature = dht.humidity, dht.temperature
            callback(humidity, temperature, settings, code)
            if stop_event.is_set():
                break
            time.sleep(delay)
