from flask import Flask
from dotenv import load_dotenv
from pathlib import Path
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient

from mqtt.client import init_mqtt
from config.settings import Config

def create_app() -> Flask:
    load_dotenv(Path(__file__).resolve().parent.parent / "infrastructure" / ".env")
    app = Flask(__name__)
    Config.init_app(app)

    influx = InfluxDBClient(
        url=app.config["INFLUX_URL"],
        token=app.config["INFLUX_TOKEN"],
        org=app.config["INFLUX_ORG"]
    )
    globals()["influx_client"] = influx

    mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION2,)
    init_mqtt(mqtt_client)
    mqtt_client.connect(app.config["MQTT_HOST"], app.config["MQTT_PORT"], 60)
    mqtt_client.loop_start()
    globals()["mqtt_client"] = mqtt

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
