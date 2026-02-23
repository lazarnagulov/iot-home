from typing import Optional
from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import DisplayState, OnOffState, RGBState
from config import PiConfig
from services.alarm_service import AlarmService
from simulators.simulation_manager import SimulationManager
from util.event_bus import SensorEvent, EventBus

def handle_command(cmd: str, 
                   registry: ActuatorRegistry, 
                   event_bus: EventBus, 
                   config: PiConfig, 
                   simulation_manager: Optional[SimulationManager] = None,
                   alarm_service: Optional[AlarmService] = None) -> str:
    parts = cmd.split()

    if parts[0] == "text" and len(parts) >= 3 and not _is_rgb_values(parts[2:]):
        name = parts[1].lower()
        text = " ".join(parts[2:]).replace("\\n", "\n")
        try:
            registry.set_state(name, DisplayState(text))
            return f"{name} is displaying '{text}'"
        except KeyError:
            return f"Unknown actuator: {name}"
        except TypeError:
            return f"Actuator { name } does not support Display State"
    
    parts = cmd.lower().split()

    if len(parts) == 4 and _is_rgb_values(parts[1:]):
        name = parts[0]
        try:
            registry.set_state(name, RGBState(r = float(parts[1]), g = float(parts[2]), b = float(parts[3])))
        except KeyError:
            return f"Unknown actuator: {name}"
        except TypeError as e:
            return e
   
    elif len(parts) == 2 and parts[1] == "on":
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
        except TypeError:
            return f"Actuator { name } does not support OnOff State"
     
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
        if len(key) != 1:
            return f"Invalid key: {key}"
        
        event = SensorEvent(
            device_info=device,
            value={"last_key": key}
        )

        event_bus.publish(event)
        return "OK"
    elif len(parts) == 2 and parts[0] == "alarm":
        if alarm_service is None:
            return "No alarm configured"
        if parts[1] == "arm":
            alarm_service.arm()
        elif parts[1] == "disarm":
            alarm_service.disarm()
        elif parts[1] == "trigger":
            alarm_service.trigger()
        else:
            return "Unknown alarm command, use 'arm', 'disarm', or 'trigger'"
        return "OK"

    elif len(parts) == 2 and parts[0] == "pause":
        if simulation_manager is not None:
            if parts[1] == "all":
                simulation_manager.pause_all()
                return "OK"
            if simulation_manager.pause(parts[1]):
                return "OK"
            else:
                return f"Failed to pause device {parts[1]}, unknown device ID"
    elif len(parts) == 2 and parts[0] == "resume":
        if simulation_manager is not None:
            if parts[1] == "all":
                simulation_manager.resume_all()
                return "OK"
            if simulation_manager.resume(parts[1]):
                return "OK"
            else:
                return f"Failed to resume device {parts[1]}, unknown device ID"
    elif len(parts) == 2 and parts[0] == "hold":
        for device_id, device_config in config.devices.items():
            if device_config.type == "button" and device_id == parts[1]:
                device = device_config
                break
        if device is None:
            return f"Device {parts[1]} not found"
        event = SensorEvent(
            device_info=device,
            value={"pressed": True},
        )
        event_bus.publish(event)
        return "OK"
    elif len(parts) == 2 and parts[0] == "release":
        for device_id, device_config in config.devices.items():
            if device_config.type == "button" and device_id == parts[1]:
                device = device_config
                break
        if device is None:
            return f"Device {parts[1]} not found"
        event = SensorEvent(
            device_info=device,
            value={"pressed": False},
        )
        event_bus.publish(event)
        return "OK"

    else:
        return "Unknown command"

def _is_rgb_values(values):
    try:
        [float(v) for v in values]
        return True
    except ValueError:
        return False