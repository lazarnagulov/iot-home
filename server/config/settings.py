import os


class Config:
    INFLUX_TOKEN: str
    INFLUX_ORG: str
    INFLUX_URL: str
    INFLUX_BUCKET: str
    MQTT_HOST: str
    MQTT_PORT: int

    SECURITY_PIN: str
    ARMING_TIME: int
    UNLOCK_ALARM_LEEWAY: int
    DOOR_LEFT_UNLOCKED_TIME_THRESHOLD: int
    GYROSCOPE_THRESHOLD: int
    PERSON_COUNT_COOLDOWN: int
    @staticmethod
    def init_config():
        Config.INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN", "")
        Config.INFLUX_ORG    = os.getenv("INFLUX_ORG", "")
        Config.INFLUX_URL    = os.getenv("INFLUX_URL", "")
        Config.INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "")
        Config.MQTT_HOST     = os.getenv("MQTT_HOST", "localhost")
        Config.MQTT_PORT     = int(os.getenv("MQTT_PORT", 1883))

        Config.SECURITY_PIN  = os.getenv("SECURITY_PIN", "1234")
        Config.ARMING_TIME   = int(os.getenv("ARMING_TIME", 10))
        Config.UNLOCK_ALARM_LEEWAY = int(os.getenv("UNLOCK_ALARM_LEEWAY", 5))
        Config.DOOR_LEFT_UNLOCKED_TIME_THRESHOLD = int(os.getenv("DOOR_LEFT_UNLOCKED_TIME_THRESHOLD", 5))
        Config.GYROSCOPE_THRESHOLD = int(os.getenv("GYROSCOPE_THRESHOLD", 5000))
        Config.PERSON_COUNT_COOLDOWN = int(os.getenv("PERSON_COUNT_COOLDOWN", 1))
