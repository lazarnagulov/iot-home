

from actuators.actuator_registry import ActuatorRegistry


def handle_command(cmd: str, registry: ActuatorRegistry) -> str:
    parts = cmd.lower().split()

    match parts:
        case [name, "on"]:
            registry.set_state(name, True)
            return f"{name} turned ON"

        case [name, "off"]:
            registry.set_state(name, False)
            return f"{name} turned OFF"

        case ["toggle", name]:
            registry.toggle(name)
            return f"{name}: {'ON' if registry.get(name).state else 'OFF'}"

        case ["status"]:
                return "\n".join(
                    f"{name}: {'ON' if act.state else 'OFF'}"
                    for name, act in registry.get_all().items()
                )

        case ["exit"]:
            return "EXIT"

        case _:
            return "Unknown command"
    
    return "Unknown command"