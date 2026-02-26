import json
import paho.mqtt.client as mqtt

from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import RGBState
from config import PiConfig

class RgbIrService:
    def __init__(self, config: PiConfig, actuator_registry: ActuatorRegistry) -> None:
        self._actuator_registry = actuator_registry
        self._config = config

        self._has_rgb_diode = False
        for device_id, device_config in config.devices.items():
            if device_config.type == "rgb_diode":
                self._has_rgb_diode = True
                self._rgb_diode_id = device_id
                break
        self._initialized = False

    def initialize(self, mqtt_client: mqtt.Client) -> None:
        if not self._has_rgb_diode:
            return
        self._mqtt_client = mqtt_client
        self._mqtt_client.message_callback_add("rgb", self.on_message)
        self._mqtt_client.subscribe("rgb")
        self._initialized = True

    def handle_ir_signal(self, key: str) -> None:
        if not self._initialized or not self._has_rgb_diode:
            return
        try:
            color = int(key)
        except ValueError:
            return
        if color < 0 or color > 7:
            return
        
        msg = {"sender": self._config.id, "color": color}
        self._mqtt_client.publish("rgb", json.dumps(msg), qos=1, retain=True)
        self.set_diode_color(color)
    
    def on_message(self, client, userdata, msg):
        try:
            msg = json.loads(msg.payload.decode())
            self.set_diode_color(msg["color"])
        except (json.JSONDecodeError, KeyError):
            pass
    
    def set_diode_color(self, color: int) -> None:
        r = 1.0 if color & 4 else 0.0
        g = 1.0 if color & 2 else 0.0
        b = 1.0 if color & 1 else 0.0

        new_state = RGBState(r, g, b)
        if self._actuator_registry.get(self._rgb_diode_id).state != new_state:
            self._actuator_registry.set_state(self._rgb_diode_id, new_state)
