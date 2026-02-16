from dataclasses import dataclass, field
import json
from typing import List

@dataclass
class DeviceConfig:
    type: str
    name: str
    simulated: bool
    id: str = field(default="")
    runs_on: str = field(default="pi1")

@dataclass
class PiConfig:
    name: str
    devices: dict[str, DeviceConfig]

@dataclass
class RGBDiodeConfig(DeviceConfig):
    red_pin: int = 12
    green_pin: int = 13
    blue_pin: int = 19
    state: str = "rgb"

@dataclass
class ButtonConfig(DeviceConfig):
    pin: int = 17
    pull_up: bool = False
    bounce_time: int = 100
    
@dataclass
class GyroscopeConfig(DeviceConfig):
    pass

@dataclass
class UltrasonicConfig(DeviceConfig):
    pins: List[int] = field(default_factory=lambda: [23, 24])
    max_iter: int = 100
    
@dataclass
class DiodeConfig(DeviceConfig):
    pin: int = 18
    state: str = "onoff"
    
@dataclass
class BuzzerConfig(DeviceConfig):
    state: str = "onoff"

@dataclass
class DHTConfig(DeviceConfig):
    pin: int = 17
    delay: float = 2.0

@dataclass
class PIRConfig(DeviceConfig):
    pin: int = 4
    
@dataclass
class IRConfig(DeviceConfig):
    delay: float = 2.0
    pin: int = 16

@dataclass
class MembraneSwitchConfig(DeviceConfig):
    row_pins: List[int] = field(default_factory=lambda: [25, 8, 7, 1])
    col_pins: List[int] = field(default_factory=lambda: [12, 16, 20, 21])
    

def load_config(config_path: str = 'config.json', pi_id: str = "pi1") -> PiConfig:
    with open(config_path, 'r') as f:
        data = json.load(f)
    
    try:
        pi_data = data[pi_id]
    except KeyError:
        raise ValueError(f"Device ID '{pi_id}' not found in configuration.")

    devices: dict[str, DeviceConfig] = {}
    for device_id, device_data in pi_data["devices"].items():
        device_id = device_id.lower()
        device_type = device_data["type"]
        if device_type == "button":
            devices[device_id] = ButtonConfig(**device_data)
        elif device_type == "ultrasonic":
            devices[device_id] = UltrasonicConfig(**device_data)
        elif device_type == "diode":
            devices[device_id] = DiodeConfig(**device_data)
        elif device_type == "buzzer":
            devices[device_id] = BuzzerConfig(**device_data)
        elif device_type == "gyro":
            devices[device_id] = GyroscopeConfig(**device_data)
        elif device_type == "pir":
            devices[device_id] = PIRConfig(**device_data)
        elif device_type == "membrane_switch":
            devices[device_id] = MembraneSwitchConfig(**device_data)
        elif device_type == "ir":
            devices[device_id] = IRConfig(**device_data)
        elif device_type == "dht":
            devices[device_id] = DHTConfig(**device_data)
        elif device_type == "rgb_diode":
            devices[device_id] = RGBDiodeConfig(**device_data)
        else:
            raise ValueError(f"Unknown device type: {device_type}")
        devices[device_id].id = device_id
        devices[device_id].runs_on = pi_id
    pi_config = PiConfig(name=pi_data["name"], devices=devices)
    return pi_config
