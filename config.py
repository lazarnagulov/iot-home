from dataclasses import dataclass
import json

@dataclass
class DS1Config:
    pin: int = 17
    pull_up: bool = False
    bounce_time: int = 100
    simulated: bool = False

@dataclass
class Config:
    ds1_config: DS1Config


def load_config(filePath: str = 'config.json') -> Config:
    with open(filePath, 'r') as f:
        data = json.load(f)
    
    ds1 = DS1Config(**data["DS1"])
    return Config(ds1_config=ds1)