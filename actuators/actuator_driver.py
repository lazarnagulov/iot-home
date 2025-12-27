import threading
from typing import Protocol

from actuators.actuator_state import ActuatorState


class ActuatorDriver(Protocol):
    
    def apply(self, state: ActuatorState) -> None: ...
    def cleanup(self) -> None: ...
    def run(self, stop_event: threading.Event) -> None: ...