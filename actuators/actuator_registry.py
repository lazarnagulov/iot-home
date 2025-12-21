import queue
from typing import Dict


class ActuatorRegistry:
    
    def __init__(self) -> None:
        self.actuators: Dict[str, queue.Queue] = {}
    
    @property
    def actuators(self) -> Dict[str, queue.Queue]:
        return self.actuators
    
    def insert_actuator(self, name: str) -> None:
        self.actuators[name] = queue.Queue()
        
    def put_command(self, name: str, command: str) -> None:
        self.actuators[name].put(command)

    def get_command_queue(self, name: str) -> queue.Queue:
        return self.actuators[name]
        