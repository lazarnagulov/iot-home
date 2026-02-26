import logging
import json
from typing import Callable, Dict, List
from actuators.actuator_registry import ActuatorRegistry
from actuators.actuator_state import OnOffState
import paho.mqtt.client as mqtt

logger = logging.getLogger("iot_home")

class ActuatorService:
    def __init__(self, mqtt_client: mqtt.Client):
        mqtt_client.message_callback_add("actuators/toggle", self.on_message)
        mqtt_client.subscribe("actuators/toggle")

    def on_message(self, client, userdata, msg):
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