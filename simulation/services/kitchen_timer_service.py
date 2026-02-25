
import json
import threading
from time import sleep

import paho.mqtt.client as mqtt

from actuators.actuator_registry import ActuatorRegistry
from config import PiConfig
from actuators.actuator_state import DisplayState
from util.logger import get_logger

logger = get_logger()

class KitchenTimerService:
    
    def __init__(self, config: PiConfig, actuator_registry: ActuatorRegistry, stop_event: threading.Event) -> None:
        self._actuator_registry = actuator_registry
        self._stop_event = stop_event
        self._config = config
        self._lock = threading.Lock()
        self._timer_thread = None
        self._timer_value = 0
        self._increment = 0
        self._running = False
        self._is_blinking = False
        
        self._has_display = False
        for device_id, device_config in config.devices.items():
            if device_config.type == "7_segment_display":
                self._has_display = True
                self._display_id = device_id
                break
        self._initialized = False

    def initialize(self, mqtt_client: mqtt.Client) -> None:
        self._mqtt_client = mqtt_client

        self._mqtt_client.subscribe("kitchen-timer")
        self._mqtt_client.message_callback_add("kitchen-timer", self.on_message)
        self._initialized = True
        
    def handle_display_state(self, device_id: str, device_name: str) -> None:
        if not self._initialized:
            return

        with self._lock:
            if self._timer_thread and self._timer_thread.is_alive():
                self._timer_value += self._increment
            elif self._is_blinking:
                self._reset_display_state()
                
        msg = {
            "id": device_id, 
            "remaining": self._timer_value , 
            "running": self._running, 
            "blinking": self._is_blinking,
            "name": device_name
        }
        self._mqtt_client.publish("kitchen-timer/state", json.dumps(msg))
    
    def on_message(self, client, userdata, msg):
        try:
            msg = json.loads(msg.payload.decode())
            if msg["command"] == "set":
                with self._lock:
                    self._increment = msg["increment"]
                    self._timer_value = msg["time"]

                if not self._timer_thread or not self._timer_thread.is_alive():
                    self._running = True
                    self._timer_thread = threading.Thread(
                        target=self.timer_thread,
                        daemon=True
                    )
                    self._timer_thread.start()
            elif msg["command"] == "reset":
                with self._lock:
                    self._reset_display_state()
            elif msg["command"] == "btn_press":
                with self._lock:
                    if self._is_blinking:
                        self._reset_display_state()
                    if self._timer_thread and self._timer_thread.is_alive():
                        self._increment = msg.get("increment", self._increment)
                        self._timer_value += self._increment
            
        except (json.JSONDecodeError, KeyError):
            pass
        
    def timer_thread(self) -> None:
        if not self._has_display or not self._display_id:
            return

        while not self._stop_event.is_set():
            with self._lock:
                if not self._running:
                    break
                to_show = self._timer_value
            
            minutes = to_show // 60
            seconds = to_show % 60
            
            display_msg = f"{minutes:02d}{seconds:02d}"
            self._actuator_registry.set_state(self._display_id, DisplayState(display_msg))
            self._mqtt_client.publish(
                "kitchen-timer/state",
                json.dumps({
                    "remaining": to_show,
                    "running": to_show > 0,
                    "blinking": to_show <= 0
                }),
                qos=1,
                retain=True
            )
            sleep(1)
            with self._lock:
                if not self._running:
                    break

                if self._timer_value > 0:
                    self._timer_value -= 1
                else:
                    self._is_blinking = True
                    self._running = False
                    break
                
    def _reset_display_state(self) -> None:
        logger.debug("Reseting display state")
        self._running = False
        self._is_blinking = False
        self._timer_value = 0
        self._increment = 0

        self._actuator_registry.set_state(self._display_id, DisplayState('reset'))
        self._mqtt_client.publish(
            "kitchen-timer/state",
            json.dumps({
                "remaining": 0,
                "running": False,
                "blinking": False
            }),
            qos=1,
            retain=True
        )