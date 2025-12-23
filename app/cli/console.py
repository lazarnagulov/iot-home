import logging
import threading
import time
from actuators.actuator_registry import ActuatorRegistry
from app.app_state import AppState
from util.command_handler import handle_command
from util.event_bus import EventBus, SensorEvent, apply_sensor_event

logger = logging.getLogger("iot_home")


def run_actuator_cli(registry: ActuatorRegistry, stop_event: threading.Event, state: AppState) -> None:
    while not stop_event.is_set():
        try:
            cmd = input().strip().lower()
            result = handle_command(cmd, registry, None)
            if result == "EXIT":
                continue
            if isinstance(result, SensorEvent):
                apply_sensor_event(state, result)
                logger.info(f"[SENSOR:{result.sensor}] {result.payload}")
            else:
                logger.info(result)
        except EOFError:
            stop_event.set()
            break
        
def run_sensor_cli(
    event_bus: EventBus,
    state: AppState,
    stop_event: threading.Event,
) -> None:
    while not stop_event.is_set():
        event: SensorEvent | None = event_bus.poll()

        if event is None:
            time.sleep(0.1)
            continue

        apply_sensor_event(state, event)

        logger.info(f"[SENSOR:{event.sensor}] {event.payload}")