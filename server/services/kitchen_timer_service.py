import json
import paho.mqtt.client as mqtt
from typing import Optional


class KitchenTimerService:

    def __init__(self, mqtt_client: mqtt.Client) -> None:
        self._mqtt_client = mqtt_client

        self._mqtt_client.message_callback_add("kitchen-timer/state", self.on_message)
        self._mqtt_client.subscribe("kitchen-timer/state")

        self.remaining: int = 0
        self.running: bool = False
        self.blinking: bool = False
        self.increment: int = 10

    def set_timer(self, time: int, increment: int) -> None:
        msg = {
            "sender": "server",
            "command": "set",
            "time": int(time),
            "increment": int(increment)
        }
        self._mqtt_client.publish(
            "kitchen-timer",
            json.dumps(msg),
            qos=1
        )

    def reset_timer(self) -> None:
        msg = {
            "sender": "server",
            "command": "reset"
        }
        self._mqtt_client.publish(
            "kitchen-timer",
            json.dumps(msg),
            qos=1
        )

    def btn_press(self, increment: int) -> None:
        msg = {
            "sender": "server",
            "command": "btn_press",
            "increment": increment
        }
        self._mqtt_client.publish(
            "kitchen-timer",
            json.dumps(msg),
            qos=1
        )

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))

            self.remaining = int(payload.get("remaining", 0))
            self.running = bool(payload.get("running", False))
            self.blinking = bool(payload.get("blinking", False))

        except (json.JSONDecodeError, KeyError, ValueError):
            pass