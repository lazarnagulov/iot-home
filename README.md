<a id="readme-top"></a>

<div align="center"> 
    <h1 align="center">IOT Home</h1> 
    <p align="center"> <br /> 
        <a href="https://github.com/lazarnagulov/iot-home/issues/new?labels=bug">Report Bug</a> 
    </p> 
</div> 

## About The Project
This project implements a smart home system across three Raspberry Pi devices, each connected to a set of sensors and actuators. Device data is collected and published via MQTT, stored in InfluxDB, and visualized through Grafana. A Flask-based web application provides a real-time dashboard for monitoring sensor readings, controlling actuators, managing a security alarm with PIN authentication, a kitchen timer, RGB lighting, live camera feed, and occupancy tracking. Simulated and physical devices are supported interchangeably through a configuration file.
<br/>

### Built With
This project uses the following core technologies:

[![Python][Python-img]][Python-url]

[![Flask][Flask-img]][Flask-url]

[![HTMX][HTMX-img]][HTMX-url]

[![Alpine.js][Alpine-img]][Alpine-url]

[![Tailwind][Tailwind-img]][Tailwind-url]

## Getting Started
Before running the project, ensure you have Python 3.10+ installed.

Check your version:
```bash
python --version
```

###  Installation Steps
1. Clone the repository:
```bash
git clone https://github.com/lazarnagulov/iot-home.git
cd iot-home
```
2. Create and activate virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```
3.  Install dependencies:
```bash
pip install -r requirements.txt
```
<br/>

## Running the Project

### Infrastructure
Start the required services (MQTT broker, InfluxDB, Grafana) using Docker Compose:
```bash
cd infrastructure
docker compose up -d
```

To stop the services:
```bash
docker compose down
```

### Server
Navigate to the server directory and start the Flask application:bashcd server
```bash
python main.py
```
The server will start and begin listening for MQTT messages, storing data to InfluxDB, and serving the web dashboard.

### Raspberry Pi
Navigate to the pi directory and run using the CLI:
```bash
cd simulation
python main.py
```
| Option | Default | Description |
|---|---|---|
| `--mode` | `tui` | Interface mode: `tui` or `cli` |
| `--config` | `./config.json` | Path to config file |
| `--device` | `pi1` | Device ID to run (`pi1`, `pi2`, `pi3`) |
| `--debug` | off | Enable debug logging |
| `--start-paused` | off | Start with all simulations paused |

### Examples
```bash
# Run PI1 in TUI mode (default)
python main.py --device pi1

# Run PI2 in CLI mode with debug logging
python main.py --device pi2 --mode cli --debug

# Run PI3 starting with simulations paused
python main.py --device pi3 --start-paused

# Use a custom config file
python main.py --device pi1 --config ./custom_config.json

# Check device configuration status
python main.py status
```
### Configuration
Each Pi is configured via config.json. A minimal device entry looks like this:
```json
{
    "pi1": {
        "name": "Raspberry Pi 1",
        "has_alarm": true,
        "devices": {
            "DS1": {
                "type": "button",
                "name": "Door Sensor 1",
                "simulated": true,
                "pin": 17
            }
        }
    }
}
```
Set `"simulated": false` on any device to use real hardware instead of simulation. 
All other devices in the config will continue to simulate normally.


[Python-img]: https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Flask-img]: https://img.shields.io/badge/Flask-3.0+-black?logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[HTMX-img]: https://img.shields.io/badge/HTMX-FF6F61?logo=htmx&logoColor=white
[HTMX-url]: https://htmx.org/
[Alpine-img]: https://img.shields.io/badge/Alpine.js-8BC0D0?logo=alpine.js&logoColor=white
[Alpine-url]: https://alpinejs.dev/
[Tailwind-img]: https://img.shields.io/badge/Tailwind%20CSS-3-38bdf8?logo=tailwindcss&logoColor=white
[Tailwind-url]: https://tailwindcss.com/