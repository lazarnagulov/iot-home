from dataclasses import dataclass, field
import json
from typing import List

@dataclass
class DeviceConfig:
    type: str
    name: str
    simulated: bool
    id: str = field(default="")

@dataclass
class PiConfig:
    name: str
    devices: dict[str, DeviceConfig]

@dataclass
class ButtonConfig(DeviceConfig):
    pin: int = 17
    pull_up: bool = False
    bounce_time: int = 100
    
@dataclass
class UltrasonicConfig(DeviceConfig):
    pins: List[int] = field(default_factory=lambda: [23, 24])
    max_iter: int = 100
    
@dataclass
class DiodeConfig(DeviceConfig):
    pin: int = 18
    
@dataclass
class BuzzerConfig(DeviceConfig):
    pass

@dataclass
class PIRConfig(DeviceConfig):
    pin: int = 4
    
@dataclass
class MembraneSwitchConfig(DeviceConfig):
    row_pins: List[int] = field(default_factory=lambda: [25, 8, 7, 1])
    col_pins: List[int] = field(default_factory=lambda: [12, 16, 20, 21])
    

def load_config(config_path: str = 'config.json', device_id: str = "pi1") -> PiConfig:
    with open(config_path, 'r') as f:
        data = json.load(f)
    
    try:
        pi_data = data[device_id]
    except KeyError:
        raise ValueError(f"Device ID '{device_id}' not found in configuration.")
    devices: dict[str, DeviceConfig] = {}
    for device_id, device_data in pi_data["devices"].items():
        device_type = device_data["type"]
        if device_type == "button":
            devices[device_id] = ButtonConfig(**device_data)
        elif device_type == "ultrasonic":
            devices[device_id] = UltrasonicConfig(**device_data)
        elif device_type == "diode":
            devices[device_id] = DiodeConfig(**device_data)
        elif device_type == "buzzer":
            devices[device_id] = BuzzerConfig(**device_data)
        elif device_type == "pir":
            devices[device_id] = PIRConfig(**device_data)
        elif device_type == "membrane_switch":
            devices[device_id] = MembraneSwitchConfig(**device_data)
        else:
            raise ValueError(f"Unknown device type: {device_type}")
        devices[device_id].id = device_id
    pi_config = PiConfig(name=pi_data["name"], devices=devices)
    return pi_config
