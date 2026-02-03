import json

from services.influx import save_to_db

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("MQTT connected")
        client.subscribe("sensors/#")
    else:
        print("MQTT connect failed:", reason_code)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    save_to_db(payload)

def init_mqtt(client):
    client.on_connect = on_connect
    client.on_message = on_message