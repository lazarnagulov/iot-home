from dataclasses import dataclass
import threading
from typing import Any, Dict

@dataclass
class CacheItem:
    name: str
    sensor_type: str
    value: Dict[str, Any]
    is_simulated: bool

    
class SensorCache:
    def __init__(self) -> None:
        self._cache: Dict[str, CacheItem] = {}
        self._lock = threading.Lock()
    
    def update(self, sensor_id: str, cache_item: CacheItem) -> None:
        with self._lock:
            self._cache[sensor_id] = cache_item
    
    def get(self, sensor_id: str) -> Any:
        with self._lock:
            return self._cache.get(sensor_id)
    
    def get_all(self) -> Dict[str, Any]:
        with self._lock:
            return self._cache.copy()