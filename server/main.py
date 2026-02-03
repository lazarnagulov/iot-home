from flask import Flask
from dotenv import load_dotenv
from pathlib import Path
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
from api.actuators import bp as actuator_bp

from mqtt.client import init_mqtt
from config.settings import Config
import config.extensions as extensions

def create_app() -> Flask:
    load_dotenv(Path(__file__).resolve().parent.parent / "infrastructure" / ".env")
    app = Flask(__name__)
    app.register_blueprint(actuator_bp)

    Config.init_config()

    influx = InfluxDBClient(
        url=Config.INFLUX_URL,
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )
    extensions.influx_client = influx

    mqtt_client_local = mqtt.Client(protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION2,)
    init_mqtt(mqtt_client_local)
    mqtt_client_local.connect(Config.MQTT_HOST, Config.MQTT_PORT, 60)
    mqtt_client_local.loop_start()
    extensions.mqtt_client = mqtt_client_local

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
