import threading

from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import OnOffState
from util.event_bus import EventBus

class DoorLightManager:
    def __init__(self, actuator_registry: ActuatorRegistry, event_bus: EventBus, stop_event: threading.Event) -> None:
        self._actuator_registry = actuator_registry
        self._event_bus = event_bus
        self._stop_event = stop_event
        self._turn_off_timer = None

    def handle_pir_state(self, state: bool) -> None:
        if state:
            self._actuator_registry.set_state("dl", OnOffState(True))
            if self._turn_off_timer is not None:
                self._turn_off_timer.cancel()
                self._turn_off_timer = None
            self._turn_off_timer = threading.Timer(10.0, self.turn_off_light)
            self._turn_off_timer.start()

    def turn_off_light(self) -> None:
        if self._stop_event.is_set():
            return
        self._actuator_registry.set_state("dl", OnOffState(False))