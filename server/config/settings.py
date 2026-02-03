import os


class Config:

    @staticmethod
    def init_app(app):
        app.config["INFLUX_TOKEN"]  = os.getenv("INFLUX_TOKEN")
        app.config["INFLUX_ORG"]    = os.getenv("INFLUX_ORG")
        app.config["INFLUX_URL"]    = os.getenv("INFLUX_URL")
        app.config["INFLUX_BUCKET"] = os.getenv("INFLUX_BUCKET")
        app.config["MQTT_HOST"]     = os.getenv("MQTT_HOST", "localhost")
        app.config["MQTT_PORT"]     = int(os.getenv("MQTT_PORT", 1883))
