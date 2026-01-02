from dataclasses import dataclass
from typing import Optional, Protocol


class ActuatorState(Protocol):

    def validate(self) -> None: ...
    def is_active(self) -> bool: ...
    def __str__(self) -> str: ...
    
@dataclass
class OnOffState(ActuatorState):
    value: bool
    
    def validate(self) -> None:
        if not isinstance(self.value, bool):
            raise TypeError("value must be boolean")
    
    def is_active(self) -> bool:
        return self.value
    
    def __str__(self) -> str:
        return "ON" if self.value else "OFF"
    
@dataclass
class RGBState(ActuatorState):
    r: float
    g: float
    b: float
    
    def validate(self) -> None:
        for name, val in [('r', self.r), ('g', self.g), ('b', self.b)]:
            if not isinstance(val, (int, float)):
                raise TypeError(f"{name} must be numeric")
            if not 0.0 <= val <= 1.0:
                raise ValueError(f"{name} must be in [0.0, 1.0]")

    def is_active(self) -> bool:
        return any(c > 0 for c in (self.r, self.g, self.b))

    
    def __str__(self) -> str:
        return f"RGB({self.r:.2f}, {self.g:.2f}, {self.b:.2f})"

@dataclass
class DisplayState(ActuatorState):
    text: str
    max_length: int = 80
    
    def validate(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError("text must be string")
        if len(self.text) > self.max_length:
            raise ValueError(f"text exceeds max length {self.max_length}")
    
    def is_active(self) -> bool:
        return bool(self.text)
    
    def __str__(self) -> str:
        return f"'{self.text}'"

@dataclass
class BuzzerState(ActuatorState):
    active: bool
    frequency: Optional[int] = None 
    duration: Optional[float] = None
    
    def validate(self) -> None:
        if self.active and self.frequency and (self.frequency < 20 or self.frequency > 20000):
            raise ValueError("frequency must be in audible range (20-20000 Hz)")
        if self.duration and self.duration < 0:
            raise ValueError("duration must be positive")
    
    def is_active(self) -> bool:
        return self.active
    
    def __str__(self) -> str:
        if not self.active:
            return "OFF"
        freq_str = f" {self.frequency}Hz" if self.frequency else ""
        dur_str = f" {self.duration}s" if self.duration else ""
        return f"ON{freq_str}{dur_str}"