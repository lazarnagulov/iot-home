import json
from typing import List
import paho.mqtt.client as mqtt

from managers.security_pin_manager import SecurityPinManager
from managers.door_lock_manager import DoorLockManager
from managers.gyro_manager import GyroManager
from managers.person_count_manager import PersonCountManager
from services.alarm_service import AlarmService
from services.sensor_cache import CacheItem
from services.influx import save_to_db
import config.extensions as extensions
from mqtt.measurement import Measurement

class MessageHandler:
    def __init__(self, mqtt_client: mqtt.Client, alarm_service: AlarmService):
        self._mqtt_client = mqtt_client
        self._alarm_service = alarm_service
        self._pin_manager = SecurityPinManager(alarm_service)
        self._door_lock_manager = DoorLockManager(alarm_service)
        self._gyro_manager = GyroManager(alarm_service)
        self._person_count_manager = PersonCountManager(alarm_service)
        alarm_service.on_alarm_state_changed(self._door_lock_manager.on_alarm_state_changed)
        alarm_service.on_alarm_state_changed(self._gyro_manager.on_alarm_state_changed)
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
                        CacheItem(measurement.name, measurement.type, measurement.id, measurement.value, measurement.simulated)
                    )
                    if measurement.type == "membrane_switch":
                        self._pin_manager.handle_key(measurement.value.get("last_key"))
                    if measurement.type == "button" and (measurement.name.startswith("Door Sensor") or measurement.id.startswith("ds")):
                        self._door_lock_manager.handle_lock_state(measurement.value.get("pressed", False))
                    if measurement.type == "gyro":
                        self._gyro_manager.handle_gyro_state(measurement.value)
                    if measurement.type == "pir":
                        if measurement.id == "dpir1":
                            distance_sensor_id = "dus1"
                        elif measurement.id == "dpir2":
                            distance_sensor_id = "dus2"
                        else:
                            distance_sensor_id = None
                        self._person_count_manager.handle_motion(measurement.id, distance_sensor_id, measurement.value.get("motion", False))
                    if measurement.type == "ultrasonic":
                        self._person_count_manager.handle_distance(measurement.id, measurement.value.get("distance", 0))
                
        except Exception as e:
            print(f"Error processing message: {e}")

    def mqtt_register_callbacks(self):
        if self.registered_callbacks:
            return
        self.registered_callbacks = True
        self._mqtt_client.message_callback_add("sensors/#", self.on_message)
        self._mqtt_client.subscribe("sensors/#")