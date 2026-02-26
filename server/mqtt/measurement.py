from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Measurement:
    id: str
    name: str
    type: str
    simulated: bool
    runs_on: str
    value: Dict[str, Any]