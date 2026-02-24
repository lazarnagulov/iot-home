import threading
import json
from time import time, sleep
import paho.mqtt.client as mqtt

from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import DisplayState, OnOffState
from config import PiConfig
from util.event_bus import EventBus

class DhtLcdService:
    def __init__(self, config: PiConfig, actuator_registry: ActuatorRegistry, stop_event: threading.Event) -> None:
        self._actuator_registry = actuator_registry
        self._stop_event = stop_event

        self._dht_values = {}
        self._lock = threading.Lock()

        self._has_lcd = False
        self._lcd_id = None
        for device_id, device_config in config.devices.items():
            if device_config.type == "lcd":
                self._has_lcd = True
                self._lcd_id = device_id
                break
        self._initialized = False

    def initialize(self, mqtt_client: mqtt.Client) -> None:
        self._mqtt_client = mqtt_client
        if self._has_lcd:
            threading.Thread(target=self.lcd_thread, daemon=True).start()
        self._initialized = True

    def handle_dht_state(self, device_id: str, device_name: str, temperature: float, humidity: float) -> None:
        if not self._initialized:
            return
        device_name = device_name.replace("DHT", "").strip()
        if len(device_name) > 15:
            device_name = device_id
        msg = {"id": device_id, "temperature": temperature, "humidity": humidity, "name": device_name}
        self._mqtt_client.publish("dht", json.dumps(msg))
    
    def on_message(self, client, userdata, msg):
        msg = json.loads(msg.payload.decode())
        msg["timestamp"] = time()
        with self._lock:
            self._dht_values[msg["id"]] = msg

    def lcd_thread(self) -> None:
        if not self._has_lcd or not self._lcd_id:
            return
        self._mqtt_client.message_callback_add("dht", self.on_message)
        self._mqtt_client.subscribe("dht")
        while not self._stop_event.is_set():
            with self._lock:
                to_show = self._dht_values.copy()
            for msg in sorted(to_show.values(), key=lambda x: x["id"]):
                if time() - msg["timestamp"] > 60:
                    continue
                name = msg["name"]
                display_msg = f"{name}:\n{msg['temperature']:.1f}C {msg['humidity']:.1f}%"
                self._actuator_registry.set_state(self._lcd_id, DisplayState(display_msg))
                sleep(3)
        