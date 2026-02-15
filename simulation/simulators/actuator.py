import threading
from typing import Callable

from actuators.actuator_registry import Actuator
from actuators.actuator_state import ActuatorState, OnOffState, RGBState
from config import DeviceConfig
from util.event_bus import EventBus, SensorEvent


def run_actuator_simulator(
    actuator: Actuator, 
    device_config: DeviceConfig,
    event_bus: EventBus,
    callback: Callable[[str, ActuatorState], None], 
    stop_event: threading.Event
) -> None:
    last_state = None
    if not isinstance(actuator.state, OnOffState):
        raise ValueError("Incompatible actuator state")

    while not stop_event.is_set():
        with actuator.lock:
            current: OnOffState = actuator.state

        if current != last_state:
            callback(actuator.name, current)
            if isinstance(current, OnOffState):
                event_bus.publish(SensorEvent(device_config, { "toggle": current.value }))
            elif isinstance(current, RGBState):
                event_bus.publish(SensorEvent(device_config, { "r": current.r, "g": current.g, "b": current.b }))
            
            last_state = current