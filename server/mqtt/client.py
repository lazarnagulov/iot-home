import json
import paho.mqtt.client as mqtt

from services.sensor_cache import CacheItem
from services.influx import save_to_db
import config.extensions as extensions


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

def mqtt_register_callbacks(client: mqtt.Client):
    client.message_callback_add("sensors/#", on_message)