import config.extensions as extensions

def send_actuator_command(name: str, state: bool) -> None:
    extensions.mqtt_client.publish(
        topic=f"actuators/{name}/set",
        payload="ON" if state else "OFF",
        qos=1,
    )