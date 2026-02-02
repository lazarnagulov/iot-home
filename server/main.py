import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask


app = Flask(__name__)
load_dotenv(Path(__file__).resolve().parent / ".env")

INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN")
INFLUX_ORG    = os.getenv("INFLUX_ORG")
INFLUX_URL    = os.getenv("INFLUX_URL")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")


if __name__ == "__main__":
    app.run()