from typing import Dict
import threading

class SimulationManager:
    def __init__(self) -> None:
        self.pause_events: Dict[str, threading.Event] = {}

    def initialize(self, pause_events: Dict[str, threading.Event]) -> None:
        self.pause_events = pause_events

    def pause(self, device_id: str) -> bool:
        if device_id in self.pause_events:
            self.pause_events[device_id].set()
            return True
        return False

    def resume(self, device_id: str) -> bool:
        if device_id in self.pause_events:
            self.pause_events[device_id].clear()
            return True
        return False
    
    def pause_all(self) -> None:
        for event in self.pause_events.values():
            event.set()
    
    def resume_all(self) -> None:
        for event in self.pause_events.values():
            event.clear()