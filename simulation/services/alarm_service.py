import logging
import json
from enum import Enum
from typing import Callable, Dict, List

import paho.mqtt.client as mqtt

from actuators.actuator_registry import ActuatorRegistry
from config import PiConfig
from actuators.actuator_state import BuzzerState

logger = logging.getLogger("iot_home")

class AlarmState(Enum):
    DISARMED = "DISARMED"
    ARMED = "ARMED"
    TRIGGERED = "TRIGGERED"

class AlarmService:
    def __init__(self, config: PiConfig, actuator_registry: ActuatorRegistry):
        self.alarm_state: AlarmState = AlarmState.DISARMED
        self.config = config
        self.actuator_registry = actuator_registry
        self.has_alarm = config.has_alarm
        self._on_alarm_state_changed: List[Callable[[], None]] = []

        if self.has_alarm:
            self.buzzers = []
            for device_id, device_config in config.devices.items():
                if device_config.type == "buzzer":
                    self.buzzers.append(device_id)

    def initialize(self, mqtt_client: mqtt.Client) -> None:
        self.mqtt_client = mqtt_client
        mqtt_client.message_callback_add("alarm/state", self._on_message)
        mqtt_client.subscribe("alarm/state")

    def arm(self):
        if self.alarm_state == AlarmState.DISARMED:
            self._publish_alarm_state(AlarmState.ARMED)

    def disarm(self):
        self._publish_alarm_state(AlarmState.DISARMED)

    def trigger(self):
        if self.alarm_state == AlarmState.ARMED:
            self._publish_alarm_state(AlarmState.TRIGGERED)

    def _publish_alarm_state(self, state: AlarmState):
        self.mqtt_client.publish("alarm/state", json.dumps({"state": state.value, "sender": self.config.id}), qos=1, retain=True)

    def _apply_state(self, new_state: AlarmState):
        logger.info(f"Alarm state changed: {self.alarm_state} -> {new_state}")
        self.alarm_state = new_state
        for callback in self._on_alarm_state_changed:
            callback()
        if self.has_alarm:
            if new_state == AlarmState.TRIGGERED:
                for buzzer_id in self.buzzers:
                    self.actuator_registry.set_state(buzzer_id, BuzzerState(True))
            else:
                for buzzer_id in self.buzzers:
                    self.actuator_registry.set_state(buzzer_id, BuzzerState(False))

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            new_state = AlarmState(payload["state"])
            if new_state != self.alarm_state:
                self._apply_state(new_state)
        except (json.JSONDecodeError, KeyError) as e:
            logger.exception("Invalid message:", e, msg.payload)

    def on_alarm_state_changed(self, callback: Callable[[], None]) -> None:
        self._on_alarm_state_changed.append(callback)