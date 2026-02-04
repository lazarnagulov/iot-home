from typing import Optional
from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import OnOffState
from config import PiConfig
from util.event_bus import SensorEvent, EventBus


def handle_command(cmd: str, registry: ActuatorRegistry, event_bus: EventBus, config: Optional[PiConfig] = None) -> str:
    parts = cmd.lower().split()

    if len(parts) == 2 and parts[1] == "on":
        name = parts[0]
        try:
            registry.set_state(name, OnOffState(value=True))
            return f"{name} turned ON"
        except KeyError:
            return f"Unknown actuator: {name}"

    elif len(parts) == 2 and parts[1] == "off":
        name = parts[0]
        try:
            registry.set_state(name, OnOffState(value=False))
            return f"{name} turned OFF"
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
        if config is None:
            return "No membrane switch configured"
        key = parts[1]
        device = None
        for _, device_config in config.devices.items():
            if device_config.type == "membrane_switch":
                device = device_config
                break
        if device is None:
            return "No membrane switch configured"
        
        event = SensorEvent(
            device_info=device,
            value={"last_key": key}
        )

        event_bus.publish(event)
        return "OK"

    else:
        return "Unknown command"
