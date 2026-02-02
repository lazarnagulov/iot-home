from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from config.extensions import influx_client
from flask import current_app

def save_to_db(data: dict):
    if not influx_client:
        raise RuntimeError("Influx client is not initialized")
        
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )

    write_api.write(
        bucket=current_app.config["INFLUX_BUCKET"],
        org=current_app.config["INFLUX_ORG"],
        record=point
    )
