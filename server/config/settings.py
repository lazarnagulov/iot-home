import os


class Config:
    INFLUX_TOKEN: str
    INFLUX_ORG: str
    INFLUX_URL: str
    INFLUX_BUCKET: str
    MQTT_HOST: str
    MQTT_PORT: int
    SECURITY_PIN: str
    @staticmethod
    def init_config():
        Config.INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN", "")
        Config.INFLUX_ORG    = os.getenv("INFLUX_ORG", "")
        Config.INFLUX_URL    = os.getenv("INFLUX_URL", "")
        Config.INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "")
        Config.MQTT_HOST     = os.getenv("MQTT_HOST", "localhost")
        Config.MQTT_PORT     = int(os.getenv("MQTT_PORT", 1883))
        Config.SECURITY_PIN  = os.getenv("SECURITY_PIN", "1234")
