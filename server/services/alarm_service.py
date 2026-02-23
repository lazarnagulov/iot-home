import json
from enum import Enum
import threading
import paho.mqtt.client as mqtt
from typing import Callable, List

from config import settings


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
        self._arming = False
        self._stop_arming = threading.Event()
        self._on_alarm_state_changed: List[Callable[[AlarmState], None]] = []

    def arm(self):
        if self._arming:
            return
        if self.alarm_state == AlarmState.DISARMED:
            self._arming = True
            threading.Timer(settings.Config.ARMING_TIME, self._finalize_arming, args=[self._stop_arming]).start()

    def disarm(self):
        if self._arming:
            self._arming = False
            self._stop_arming.set()
        self._publish_alarm_state(AlarmState.DISARMED)

    def trigger(self, force: bool = False):
        if self.alarm_state == AlarmState.ARMED or force:
            self._publish_alarm_state(AlarmState.TRIGGERED)

    def swap_state(self):
        if self.alarm_state == AlarmState.DISARMED:
            self.arm()
        else:
            self.disarm()

    def _finalize_arming(self, stop_event: threading.Event):
        if not stop_event.is_set():
            self._arming = False
            self._publish_alarm_state(AlarmState.ARMED)

    def _publish_alarm_state(self, state: AlarmState):
        self._mqtt_client.publish("alarm/state", json.dumps({"state": state.value, "sender": "server"}), qos=1, retain=True)

    def _apply_state(self, new_state: AlarmState):
        self.alarm_state = new_state
        for callback in self._on_alarm_state_changed:
            callback(new_state)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            new_state = AlarmState(payload["state"])
            if new_state != self.alarm_state:
                self._apply_state(new_state)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Invalid message: {e}", msg.payload)

    def on_alarm_state_changed(self, callback: Callable[[AlarmState], None]) -> None:
        self._on_alarm_state_changed.append(callback)