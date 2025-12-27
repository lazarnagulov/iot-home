from dataclasses import dataclass, field
import queue
import threading
from typing import Dict

from actuators.actuator_state import ActuatorState, OnOffState

@dataclass
class Actuator:
    name: str
    state: ActuatorState
    lock: threading.Lock = field(default_factory=threading.Lock)
    commands: queue.Queue[ActuatorState] = field(default_factory=queue.Queue)

class ActuatorRegistry:

    def __init__(self) -> None:
        self._actuators: Dict[str, Actuator] = {}

    def register(self, name: str) -> Actuator:
        if name in self._actuators:
            raise ValueError(f"Actuator '{name}' already registered")

        actuator = Actuator(name=name, state=OnOffState(value=False))
        self._actuators[name] = actuator
        return actuator

    def get(self, name: str) -> Actuator:
        return self._actuators[name]

    def set_state(self, name: str, state: ActuatorState) -> None:
        actuator = self.get(name)
        state.validate()

        with actuator.lock:
            actuator.state = state
            actuator.commands.put(state)

    def get_all(self) -> Dict[str, Actuator]:
        return self._actuators
