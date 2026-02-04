import threading
from typing import Callable

from actuators.actuator_registry import Actuator
from actuators.actuator_state import ActuatorState
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

    while not stop_event.is_set():
        with actuator.lock:
            current = actuator.state

        if current != last_state:
            callback(actuator.name, current)
            event_bus.publish(SensorEvent(device_config, { "toggle": current.value }))
            last_state = current