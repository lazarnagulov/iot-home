from dataclasses import dataclass
import json
import queue
import threading
from typing import Any, Dict, Optional
import paho.mqtt.publish as publish

from app.app_state import AppState
from config import DeviceConfig
from broker_settings import HOSTNAME, PORT
from util.logger import get_logger

logger = get_logger()

class SensorEvent:
    def __init__(self, device_info: DeviceConfig, value: Dict[str, Any]) -> None:
        self.sensor = device_info.id
        self.payload: Dict[str, Any] = {}
        self.payload["value"] = value
        self.payload["id"] = device_info.id
        self.payload["type"] = device_info.type
        self.payload["name"] = device_info.name
        self.payload["simulated"] = device_info.simulated
        self.payload["runs_on"] = device_info.runs_on


class EventBus:
    def __init__(self) -> None:
        self._queue: queue.Queue = queue.Queue()
        self._poll_queue: queue.Queue = queue.Queue()
        self._batch_size = 64

        self._thread = threading.Thread(target=self.publish_task, daemon=True)
        self._thread.start()

    def publish(self, event: SensorEvent) -> None:
        self._queue.put(event)
        self._poll_queue.put(event)

    def poll(self) -> Optional[SensorEvent]:
        try:
            if self._queue.qsize() >= self._batch_size:
                self._sending = True
                send = True
            return self._poll_queue.get_nowait()
        except queue.Empty:
            return None
        
    def publish_task(self) -> None:
        while True:
            if self._queue.qsize() < self._batch_size:
                continue
            buffer = []
            for _ in range(self._batch_size):
                try:
                    buffer.append(self._queue.get_nowait())
                except queue.Empty:
                    break
            if buffer:
                msgs = []
                for event in buffer:
                    msg = {
                        "topic": "sensors/data",
                        "payload": json.dumps(event.payload),
                        "qos": 1
                    }
                    msgs.append(msg)
                publish.multiple(msgs, hostname=HOSTNAME, port=PORT)
                logger.debug(f"Published batch of {len(buffer)} sensor events")
        
            
            
            
        
def apply_sensor_event(state: AppState, event: SensorEvent) -> None:
    sensor = state.sensors.setdefault(event.sensor, {})
    sensor.update(event.payload)
