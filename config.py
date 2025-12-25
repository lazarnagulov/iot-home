from dataclasses import dataclass, field
import json
from typing import List

@dataclass
class DS1Config:
    pin: int = 17
    pull_up: bool = False
    bounce_time: int = 100
    simulated: bool = False
    
@dataclass
class DUS1Config:
    pins: List[int] = field(default_factory=lambda: [23, 24])
    simulated: bool = False
    max_iter: int = 100
    
@dataclass
class DLConfig:
    simulated: bool = False
    
@dataclass
class DBConfig:
    simulated: bool = False

@dataclass
class DPIR1Config:
    pin: int = 4
    simulated: bool = False
    
@dataclass
class DMSConfig:
    row_pins: List[int] = field(default_factory=lambda: [25, 8, 7, 1])
    col_pins: List[int] = field(default_factory=lambda: [12, 16, 20, 21])
    simulated: bool = False
    
@dataclass
class Config:
    ds1_config: DS1Config
    dus1_config: DUS1Config
    dl_config: DLConfig
    db_config: DBConfig
    dpir1_config: DPIR1Config
    dms_config: DMSConfig


def load_config(config_path: str = 'config.json') -> Config:
    with open(config_path, 'r') as f:
        data = json.load(f)
    
    ds1 = DS1Config(**data["DS1"])
    dus1 = DUS1Config(**data["DUS1"])
    dl = DLConfig(**data["DL"])
    db = DBConfig(**data["DB"])
    dpir1 = DPIR1Config(**data["DPIR1"])
    dms = DMSConfig(**data["DMS"])
    return Config(ds1_config=ds1, dus1_config=dus1, dl_config=dl, db_config=db, dpir1_config=dpir1, dms_config=dms)
