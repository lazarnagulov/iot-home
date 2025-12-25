from typing import Optional
from actuators.actuator_registry import ActuatorRegistry
from util.event_bus import SensorEvent, EventBus


def handle_command(cmd: str, registry: ActuatorRegistry, event_bus: Optional[EventBus]) -> str | SensorEvent:
    parts = cmd.lower().split()

    if len(parts) == 2 and parts[1] == "on":
        name = parts[0]
        try:
            registry.set_state(name, True)
            return f"{name} turned ON"
        except KeyError:
            return f"Unknown actuator: {name}"

    elif len(parts) == 2 and parts[1] == "off":
        name = parts[0]
        try:
            registry.set_state(name, False)
            return f"{name} turned OFF"
        except KeyError:
            return f"Unknown actuator: {name}"

    elif len(parts) == 2 and parts[0] == "toggle":
        name = parts[1]
        try:
            registry.toggle(name)
            return f"{name}: {'ON' if registry.get(name).state else 'OFF'}"
        except KeyError:
            return f"Unknown actuator: {name}"

    elif len(parts) == 1 and parts[0] == "status":
        return "\n".join(
            f"{name}: {'ON' if act.state else 'OFF'}"
            for name, act in registry.get_all().items()
        )

    elif len(parts) == 1 and parts[0] == "exit":
        return "EXIT"

    elif len(parts) == 2 and parts[0] == "press":
        key = parts[1]
        event = SensorEvent(
            sensor="DMS",
            payload={"last_key": key}
        )

        if event_bus is None:
            return event
        else:
            event_bus.publish(event)
            return "OK"

    else:
        return "Unknown command"
