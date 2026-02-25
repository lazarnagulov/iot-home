
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
        
    def handle_display_state(self, device_id: str, device_name: str, timer_value: str) -> None:
        if not self._initialized:
            return
    
    def on_message(self, client, userdata, msg):
        try:
            msg = json.loads(msg.payload.decode())
            if msg["command"] == "set":
                with self._lock:
                    self._increment = msg["increment"]
                    self._timer_value = msg["time"]

                if not self._timer_thread or not self._timer_thread.is_alive():
                    self._timer_thread = threading.Thread(
                        target=self.timer_thread,
                        daemon=True
                    )
                    self._timer_thread.start()
            elif msg["command"] == "reset":
                with self._lock:
                    self._increment = 0
                    self._timer_value = 0
                    self._actuator_registry.set_state(self._display_id, DisplayState('reset'))
            elif msg["command"] == "btn_press":
                with self._lock:
                    self._timer_value += self._increment
            
        except (json.JSONDecodeError, KeyError):
            pass
        
    def timer_thread(self) -> None:
        if not self._has_display or not self._display_id:
            return

        self._mqtt_client.message_callback_add("kitchen-timer/state", self.on_message)
        self._mqtt_client.subscribe("kitchen-timer/state")
        while not self._stop_event.is_set():
            with self._lock:
                to_show = self._timer_value
            
            minutes = to_show // 60
            seconds = to_show % 60
            
            display_msg = f"{minutes:02d}{seconds:02d}"
            self._actuator_registry.set_state(self._display_id, DisplayState(display_msg))
            sleep(1)
            with self._lock:
                if self._timer_value > 0:
                    self._timer_value -= 1
                else:
                    break