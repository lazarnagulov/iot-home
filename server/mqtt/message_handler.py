import json
from typing import List
import paho.mqtt.client as mqtt

from managers.security_pin_manager import SecurityPinManager
from services.sensor_cache import CacheItem
from services.influx import save_to_db
import config.extensions as extensions
from mqtt.measurement import Measurement

class MessageHandler:
    def __init__(self, mqtt_client: mqtt.Client):
        self._mqtt_client = mqtt_client
        self._pin_manager = SecurityPinManager()
        self.registered_callbacks = False
        self.mqtt_register_callbacks()

    def on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            data = json.loads(msg.payload.decode())
            if topic.startswith("sensors/"):
                payload: List[Measurement] = [Measurement(**item) for item in data]
                for measurement in payload:
                    save_to_db(measurement)
                    extensions.sensor_cache.update(
                        measurement.id,
                        CacheItem(measurement.name, measurement.type, measurement.value, measurement.simulated)
                    )
                    if measurement.type == "membrane_switch":
                        self._pin_manager.process_key(measurement.value.get("last_key"))

                
        except Exception as e:
            print(f"Error processing message: {e}")

    def mqtt_register_callbacks(self):
        if self.registered_callbacks:
            return
        self.registered_callbacks = True
        self._mqtt_client.message_callback_add("sensors/#", self.on_message)