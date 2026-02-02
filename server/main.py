import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json


app = Flask(__name__)
load_dotenv(Path(__file__).resolve().parent.parent / "infrastructure" / ".env")

INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN")
INFLUX_ORG    = os.getenv("INFLUX_ORG")
INFLUX_URL    = os.getenv("INFLUX_URL")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

def on_connect(client):
    print(f"Client { client } connected")
    ...

def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field("measurement", data["value"])
    )
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()
mqtt_client.on_connect = lambda client, userdata, flags, rc: on_connect(client)
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))


if __name__ == "__main__":
    app.run()