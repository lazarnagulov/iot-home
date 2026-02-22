from typing import Optional
from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt

from services.sensor_cache import SensorCache

influx_client: Optional[InfluxDBClient] = None
mqtt_client:   Optional[mqtt.Client]    = None
sensor_cache:  Optional[SensorCache]    = None