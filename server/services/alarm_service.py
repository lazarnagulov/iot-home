import json
from enum import Enum
import paho.mqtt.client as mqtt


class AlarmState(Enum):
    DISARMED = "DISARMED"
    ARMED = "ARMED"
    TRIGGERED = "TRIGGERED"

    
class AlarmService:
    def __init__(self, mqtt_client: mqtt.Client):
        self.alarm_state: AlarmState = AlarmState.DISARMED

        self._mqtt_client = mqtt_client
        self._mqtt_client.message_callback_add("alarm/state", self._on_message)
        self._mqtt_client.subscribe("alarm/state")

    def arm(self):
        if self.alarm_state == AlarmState.DISARMED:
            self._publish_alarm_state(AlarmState.ARMED)

    def disarm(self):
        self._publish_alarm_state(AlarmState.DISARMED)

    def trigger(self):
        if self.alarm_state == AlarmState.ARMED:
            self._publish_alarm_state(AlarmState.TRIGGERED)

    def _publish_alarm_state(self, state: AlarmState):
        self._mqtt_client.publish("alarm/state", json.dumps({"state": state.value, "sender": "server"}), qos=1, retain=True)

    def _apply_state(self, new_state: AlarmState):
        self.alarm_state = new_state

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            new_state = AlarmState(payload["state"])
            if new_state != self.alarm_state:
                self._apply_state(new_state)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Invalid message: {e}", msg.payload)