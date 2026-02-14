import threading
import time
from sensors.MPU.MPU6050 import MPU6050
from config import GyroscopeConfig
from util.event_bus import EventBus, SensorEvent

class Gyroscope:
    
    def __init__(self, config: GyroscopeConfig, event_bus: EventBus) -> None:
        self._mpu = MPU6050() 
        self._accel = [0]*3 
        self._gyro = [0]*3
        self._config = config
        self._event_bus = event_bus
        
    def run(self, stop_event: threading.Event) -> None:
        while not stop_event.is_set():
            accel = self._mpu.get_acceleration() 
            gyro = self._mpu.get_rotation()

            self._event_bus.publish(
                SensorEvent(
                    device_info=self._config,
                    value={
                        "accel_x": accel[0],
                        "accel_y": accel[1],
                        "accel_z": accel[2],
                        "gyro_x": gyro[0],
                        "gyro_y": gyro[1],
                        "gyro_z": gyro[2],
                    },
                )
            )
            time.sleep(0.1)
        