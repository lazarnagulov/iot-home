import threading

from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import OnOffState
from util.event_bus import EventBus

class DoorLightManager:
    def __init__(self, actuator_registry: ActuatorRegistry, event_bus: EventBus) -> None:
        self._actuator_registry = actuator_registry
        self._event_bus = event_bus
        self._turn_off_timer = None

    def handle_pir_state(self, state: bool) -> None:
        if state:
            self._actuator_registry.set_state("dl", OnOffState(True))
            if self._turn_off_timer is not None:
                self._turn_off_timer.cancel()
                self._turn_off_timer = None
            self._turn_off_timer = threading.Timer(10.0, lambda: self._actuator_registry.set_state("dl", OnOffState(False)))
            self._turn_off_timer.start()