import threading
from actuators.actuator_registry import ActuatorRegistry
from util.logger import log_message

def run_actuator_cli(registry: ActuatorRegistry, stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        try:
            cmd = input().strip().lower()
            parts = cmd.split()

            match parts:
                case [name, "on"]:
                    registry.set_state(name, True)

                case [name, "off"]:
                    registry.set_state(name, False)

                case ["toggle", name]:
                    registry.toggle(name)

                case ["status"]:
                    for name, act in registry.get_all().items():
                        print(f"{name}: {'ON' if act.state else 'OFF'}")

                case _:
                    log_message("Unknown command")
        except EOFError:
            stop_event.set()
            break