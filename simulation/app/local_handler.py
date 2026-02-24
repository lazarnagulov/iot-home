import threading

from managers.door_light_manager import DoorLightManager
from actuators.actuator_registry import ActuatorRegistry
from services.dht_lcd_service import DhtLcdService
from util.event_bus import EventBus

def run_local_handler(event_bus: EventBus, actuator_registry: ActuatorRegistry, dht_lcd_service: DhtLcdService, stop_event: threading.Event) -> None:
    threading.Thread(target = _handle_events, args=(event_bus, actuator_registry, dht_lcd_service, stop_event)).start()

def _handle_events(event_bus: EventBus, actuator_registry: ActuatorRegistry, dht_lcd_service: DhtLcdService, stop_event: threading.Event) -> None:
    door_light_manager = DoorLightManager(actuator_registry, event_bus, stop_event)
    while not stop_event.is_set():
        event = event_bus.handler_poll()
        if event is not None:
            if event.sensor == "dpir1":
                door_light_manager.handle_pir_state(event.payload["value"].get("motion", False))
            elif event.payload["type"] == "dht":
                try:
                    dht_lcd_service.handle_dht_state(event.sensor, event.payload["name"], event.payload["value"]["temperature"], event.payload["value"]["humidity"])
                except KeyError:
                    pass