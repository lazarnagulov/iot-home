from dataclasses import dataclass, field
from typing import Any, Dict

from actuators.actuator_registry import ActuatorRegistry

@dataclass
class AppState:
    sensors: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    actuator_registry: ActuatorRegistry = field(default_factory=dict)