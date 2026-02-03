from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import config.extensions as extensions
from config.settings import Config

def save_to_db(data: dict):
    if not extensions.influx_client:
        raise RuntimeError("Influx client is not initialized")
        
    write_api = extensions.influx_client.write_api(write_options=SYNCHRONOUS)

    value = {
        "tags": {
            "simulated": data["simulated"],
            "runs_on": data["runs_on"],
            "name": data["name"],
            "type": data["type"],
        },
        "fields": data["value"],
        "measurement": data["id"]
    }

    point = (
        Point.from_dict(value)
        # .tag("simulated", data["simulated"])
        # .tag("runs_on", data["runs_on"])
        # .tag("name", data["name"])
        # .tag("type", data["type"])
        # .from_dict(data["value"])
        # .field("id", data["id"])
    )

    write_api.write(
        bucket=Config.INFLUX_BUCKET,
        org=Config.INFLUX_ORG,
        record=point
    )
