import json
import paho.mqtt.client as mqtt

class RgbService:
    def __init__(self, mqtt_client: mqtt.Client) -> None:
        self._mqtt_client = mqtt_client
        self._mqtt_client.message_callback_add("rgb", self.on_message)
        self._mqtt_client.subscribe("rgb")
        self.r = 0
        self.g = 0
        self.b = 0

    def update_color(self, r: int, g: int, b: int) -> None:
        r = 1 if int(r) > 0 else 0
        g = 1 if int(g) > 0 else 0
        b = 1 if int(b) > 0 else 0
        color = r * 4 + g * 2 + b
        msg = {"sender": "server", "color": color}
        self._mqtt_client.publish("rgb", json.dumps(msg), qos=1, retain=True)
        self.r = r
        self.g = g 
        self.b = b
    
    def on_message(self, client, userdata, msg):
        try:
            msg = json.loads(msg.payload.decode())
            color = msg["color"]
            self.r = 1 if color & 4 else 0
            self.g = 1 if color & 2 else 0
            self.b = 1 if color & 1 else 0

        except (json.JSONDecodeError, KeyError):
            pass
