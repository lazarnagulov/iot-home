from typing import Dict
from actuators.base import Actuator


class ActuatorRegistry:

    def __init__(self) -> None:
        self._actuators: Dict[str, Actuator] = {}

    def register(self, name: str) -> Actuator:
        if name in self._actuators:
            raise ValueError(f"Actuator '{name}' already registered")

        actuator = Actuator(name=name)
        self._actuators[name] = actuator
        return actuator

    def get(self, name: str) -> Actuator:
        return self._actuators[name]

    def set_state(self, name: str, value: bool) -> None:
        actuator = self.get(name)
        with actuator.lock:
            actuator.state = value

    def toggle(self, name: str) -> None:
        actuator = self.get(name)
        with actuator.lock:
            actuator.state = not actuator.state

    def get_all(self) -> Dict[str, Actuator]:
        return self._actuators
