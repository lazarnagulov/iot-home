from dataclasses import dataclass, field
from typing import Dict

from actuators.actuator_registry import ActuatorRegistry
from actuators.base import Actuator

@dataclass
class AppState:
    sensors: Dict[str, dict] = field(default_factory=dict)
    actuator_registry: ActuatorRegistry = field(default_factory=dict)