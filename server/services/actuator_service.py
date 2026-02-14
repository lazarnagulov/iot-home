import json
import config.extensions as extensions

def send_actuator_command(name: str) -> None:
    extensions.mqtt_client.publish(
        topic="actuators/toggle",
        payload=json.dumps({"name": name}),
        qos=1,
    )