import threading
from typing import Callable

from actuators.actuator_registry import Actuator
from actuators.actuator_state import ActuatorState


def run_actuator_simulator(
    actuator: Actuator, 
    callback: Callable[[str, ActuatorState], None], 
    stop_event: threading.Event
) -> None:
    last_state = None

    while not stop_event.is_set():
        with actuator.lock:
            current = actuator.state

        if current != last_state:
            callback(actuator.name, current)
            last_state = current