import json

from services.sensor_cache import CacheItem
from services.influx import save_to_db
import config.extensions as extensions

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("MQTT connected")
        client.subscribe("sensors/#")
    else:
        print("MQTT connect failed:", reason_code)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        if topic.startswith("sensors/"):
            for measurement in payload:
                save_to_db(measurement)
                extensions.sensor_cache.update(
                    measurement["id"],
                    CacheItem(measurement['name'], measurement['type'], measurement['value'], measurement['simulated'])
                )
            
    except Exception as e:
        print(f"Error processing message: {e}")

def init_mqtt(client):
    client.on_connect = on_connect
    client.on_message = on_message