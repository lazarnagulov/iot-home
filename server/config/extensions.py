import threading
import time
from typing import Optional
from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt

influx_client: Optional[InfluxDBClient] = None
mqtt_client: Optional[mqtt.Client]      = None