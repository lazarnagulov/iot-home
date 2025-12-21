import threading
from actuators.actuator_registry import ActuatorRegistry
from util.command_handler import handle_command
from util.logger import log_message

def run_actuator_cli(registry: ActuatorRegistry, stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        try:
            cmd = input().strip().lower()
            result = handle_command(cmd, registry)
            if result == "EXIT":
                continue
            log_message(result)
        except EOFError:
            stop_event.set()
            break