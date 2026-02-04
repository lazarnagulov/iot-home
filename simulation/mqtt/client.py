import json

from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import OnOffState
from util.logger import get_logger

logger = get_logger()

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logger.info("MQTT connected")
        client.subscribe("actuators/#")
    else:
        logger.exception("MQTT connect failed:", reason_code)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        name = payload["name"]
        logger.debug(f"Actuator toggle requested: {name}")

        registry: ActuatorRegistry = userdata
        actuator = registry.get(name)
        if not actuator:
            logger.error(f"Actuator { name } not found")
            return
        new_state = OnOffState(not actuator.state.is_active)
        actuator.state = new_state
        logger.info(f"{name} is now {'ON' if new_state.is_active else 'OFF'}")
        
    except (json.JSONDecodeError, KeyError) as e:
        logger.exception("Invalid message:", e, msg.payload)
        
def init_mqtt(client):
    client.on_connect = on_connect
    client.on_message = on_message