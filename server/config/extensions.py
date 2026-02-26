from typing import Optional
from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt

from services.kitchen_timer_service import KitchenTimerService
from services.rgb_service import RgbService
from services.alarm_service import AlarmService
from services.sensor_cache import SensorCache
from mqtt.message_handler import MessageHandler

influx_client:        Optional[InfluxDBClient]      = None
mqtt_client:          Optional[mqtt.Client]         = None
sensor_cache:         Optional[SensorCache]         = None
alarm_service:        Optional[AlarmService]        = None
message_handler:      Optional[MessageHandler]      = None
rgb_service:          Optional[RgbService]          = None
kitech_timer_service: Optional[KitchenTimerService] = None