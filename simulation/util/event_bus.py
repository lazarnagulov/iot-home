from dataclasses import dataclass
import queue
from typing import Any, Dict, Optional

from app.app_state import AppState

@dataclass(frozen=True)
class SensorEvent:
    sensor: str
    payload: Dict[str, Any]

class EventBus:
    def __init__(self) -> None:
        self._queue: queue.Queue = queue.Queue()

    def publish(self, event: SensorEvent) -> None:
        self._queue.put(event)

    def poll(self) -> Optional[SensorEvent]:
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None
        
def apply_sensor_event(state: AppState, event: SensorEvent) -> None:
    sensor = state.sensors.setdefault(event.sensor, {})
    sensor.update(event.payload)