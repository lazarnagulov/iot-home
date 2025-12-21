import logging
import threading
from actuators.actuator_registry import ActuatorRegistry
from util.command_handler import handle_command

logger = logging.getLogger("iot_home")


def run_actuator_cli(registry: ActuatorRegistry, stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        try:
            cmd = input().strip().lower()
            result = handle_command(cmd, registry)
            if result == "EXIT":
                continue
            logger.info(result)
        except EOFError:
            stop_event.set()
            break