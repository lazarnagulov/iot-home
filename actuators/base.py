import threading
import queue
from dataclasses import dataclass, field


@dataclass
class Actuator:
    name: str
    state: bool = False
    lock: threading.Lock = field(default_factory=threading.Lock)
    commands: queue.Queue[str] = field(default_factory=queue.Queue)
