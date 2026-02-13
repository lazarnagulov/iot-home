

import threading
from actuators.actuator_driver import ActuatorDriver
from actuators.actuator_state import ActuatorState


class RGBDiode(ActuatorDriver):
    
    def apply(self, state: ActuatorState) -> None: ...
    
    def cleanup(self) -> None: ...
    
    def run(self, stop_event: threading.Event) -> None: ...