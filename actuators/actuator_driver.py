from typing import Protocol

from actuators.actuator_state import ActuatorState


class ActuatorDriver(Protocol):
    
    def apply(self, state: ActuatorState) -> None: ...
    def cleanup(self) -> None: ...