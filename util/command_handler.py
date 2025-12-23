

from actuators.actuator_registry import ActuatorRegistry
from util.event_bus import SensorEvent, EventBus


def handle_command(cmd: str, registry: ActuatorRegistry, event_bus: EventBus) -> str:
    parts = cmd.lower().split()

    match parts:
        case [name, "on"]:
            try:
                registry.set_state(name, True)
                return f"{name} turned ON"
            except KeyError:
                return f"Unknown actuator: {name}"

        case [name, "off"]:
            try:
                registry.set_state(name, False)
                return f"{name} turned OFF"
            except KeyError:
                return f"Unknown actuator: {name}"

        case ["toggle", name]:
            try:
                registry.toggle(name)
                return f"{name}: {'ON' if registry.get(name).state else 'OFF'}"
            except KeyError:
                return f"Unknown actuator: {name}"

        case ["status"]:
                return "\n".join(
                    f"{name}: {'ON' if act.state else 'OFF'}"
                    for name, act in registry.get_all().items()
                )

        case ["exit"]:
            return "EXIT"
        
        case ["press", key]:    
            if event_bus is None:
                return SensorEvent(
                        sensor="DMS",
                        payload={ "last_key": f"{ key }" }
                    )
            else:
                event_bus.publish(
                    SensorEvent(
                        sensor="DMS",
                        payload={ "last_key": f"{ key }" }
                    )
                )

        case _:
            return "Unknown command"
    
    return "Unknown command"