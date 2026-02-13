import math
import time
import threading

from config import GyroscopeConfig
from util.event_bus import EventBus, SensorEvent


_start_time = time.time()

def _simulate_motion():
    t = time.time() - _start_time

    ax = math.sin(t) * 0.2
    ay = math.cos(t * 0.7) * 0.2
    az = 1.0

    gx = math.sin(t * 1.5) * 50
    gy = math.cos(t * 1.2) * 50
    gz = math.sin(t * 0.8) * 50

    return ax, ay, az, gx, gy, gz


def run_gyroscope_simulator(
    config: GyroscopeConfig,
    delay: float,
    event_bus: EventBus,
    stop_event: threading.Event
) -> None:
    while not stop_event.is_set():
        time.sleep(delay)

        if stop_event.is_set():
            break

        ax, ay, az, gx, gy, gz = _simulate_motion()
        accel_raw = [int(ax * 16384), int(ay * 16384), int(az * 16384)]
        gyro_raw = [int(gx * 131), int(gy * 131), int(gz * 131)]

        event_bus.publish(
            SensorEvent(
                device_info=config,
                value={
                    "accel_x": accel_raw[0],
                    "accel_y": accel_raw[1],
                    "accel_z": accel_raw[2],
                    "gyro_x": gyro_raw[0],
                    "gyro_y": gyro_raw[1],
                    "gyro_z": gyro_raw[2],
                },
            )
        )
