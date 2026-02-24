import logging
import threading
from typing import Any, Callable, Dict, List

from actuators.actuator_registry import ActuatorRegistry
from app.app_state import AppState
from components.diode import run_diode
from components.buzzer import run_buzzer
from components.button import run_button
from components.ultrasonic import run_ultrasonic
from components.pir import run_pir
from components.dht import run_dht
from components.membrane_switch import run_membrane_switch
from components.infrared import run_infrared
from components.seven_segment import run_seven_segment_display
from components.lcd import run_lcd
from components.rgb_diode import run_rgb_diode
from components.gyroscope import run_gyroscope

from config import DeviceConfig, PiConfig
from app.local_handler import run_local_handler
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT
from actuators.actuator_state import DisplayState, RGBState
from services.dht_lcd_service import DhtLcdService
from services.rgb_ir_service import RgbIrService
from simulators.simulation_manager import SimulationManager
from util.event_bus import EventBus
from services.actuator_service import ActuatorService
from services.alarm_service import AlarmService

logger = logging.getLogger("iot_home")

try:
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource] # ty: ignore[unresolved-import]
    GPIO.setmode(GPIO.BCM)
except (ModuleNotFoundError, RuntimeError):
    pass

type ActuatorFn = Callable[[DeviceConfig, ActuatorRegistry, EventBus, List[threading.Thread], threading.Event], None]
type SensorFn   = Callable[[DeviceConfig, EventBus, List[threading.Thread], threading.Event, threading.Event], None]

class SystemManager:
    
    def __init__(self, config: PiConfig, start_paused: bool = False):
        self.config = config
        self.threads: List[threading.Thread] = []
        self.stop_event = threading.Event()
        self.mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION2,)
        self.event_bus = EventBus(self.mqtt_client)
        self.actuator_registry = ActuatorRegistry()
        self.simulation_manager = SimulationManager()
        self.state = AppState(
            sensors={},
            actuator_registry= self.actuator_registry,
        )
        self.start_paused = start_paused
        self.sensor_functions: Dict[str, SensorFn] = {
            "button": run_button,
            "ultrasonic": run_ultrasonic,
            "pir": run_pir,
            "membrane_switch": run_membrane_switch,
            "ir": run_infrared,
            "dht": run_dht,
            "gyro": run_gyroscope,
        }
        self.actuator_functions: Dict[str, ActuatorFn] = {
            "diode": run_diode,
            "rgb_diode": run_rgb_diode,
            "buzzer": run_buzzer,
            "7_segment_display": run_seven_segment_display,
            "lcd": run_lcd
        }
        self.alarm_service = AlarmService(config, self.actuator_registry)
        self.dht_lcd_service = DhtLcdService(config, self.actuator_registry, self.stop_event)
        self.rgb_ir_service = RgbIrService(config, self.actuator_registry)
        
    def initialize(self) -> None:
        logger.info("Initializing system components...")

        self.mqtt_client.user_data_set(self.actuator_registry)
        self.mqtt_client.on_connect = self.on_mqtt_connect
        try:
            self.mqtt_client.connect(HOSTNAME, PORT, 60)
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise
        self.mqtt_client.loop_start()
        
        for device_id, device_config in self.config.devices.items():
            device_type = device_config.type
            if self.is_actuator(device_type):
                
                if device_config.state == "rgb":
                    self.state.actuator_registry.register(device_id, RGBState(0,0,0))
                elif device_config.state == "display":
                    self.state.actuator_registry.register(device_id, DisplayState(text="Test"))
                else:
                    self.state.actuator_registry.register(device_id)
        
        try:
            pause_events: Dict[str, threading.Event] = {}
            for device_id, device_config in self.config.devices.items():
                device_type = device_config.type
                if self.is_sensor(device_type):
                    run_function = self.sensor_functions[device_type]
                    pause_event = threading.Event()
                    pause_events[device_id] = pause_event
                    if self.start_paused:
                        pause_event.set()
                    run_function(device_config, self.event_bus, self.threads, self.stop_event, pause_event)
                elif self.is_actuator(device_type):
                    run_function = self.actuator_functions[device_type]
                    run_function(device_config, self.state.actuator_registry, self.event_bus,  self.threads, self.stop_event)
                else:
                    raise ValueError(f"Unknown device type: {device_type}")
            
            self.simulation_manager.initialize(pause_events)
            run_local_handler(self.event_bus, self.state.actuator_registry, self.dht_lcd_service, self.rgb_ir_service, self.stop_event)
            logger.info(f"System initialized with {len(self.threads)} components")
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            self.stop_event.set()
            raise
    
    def shutdown(self) -> None:
        logger.info("Shutting down system...")
        self.stop_event.set()
        
        for thread in self.threads:
            thread.join(timeout=2.0)
            if thread.is_alive():
                logger.warning(f"Thread {thread.name} did not stop gracefully")
        
        try:
            GPIO.cleanup()
            logger.debug("GPIO cleaned up")
        except NameError:
            pass
        logger.info("System shutdown complete")
        
    
    def get_status(self) -> dict:
        return {
            "threads_running": sum(1 for t in self.threads if t.is_alive()),
            "total_threads": len(self.threads),
            "actuators": len(self.state.actuator_registry.get_all()),
            "stop_requested": self.stop_event.is_set(),
        }
    
    def is_actuator(self, device_id: str) -> bool:
        return device_id in self.actuator_functions.keys()
    
    def is_sensor(self, device_id: str) -> bool:
        return device_id in self.sensor_functions.keys()
    
    def on_mqtt_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logger.info("MQTT connected")
            self.actuator_service = ActuatorService(client)
            self.alarm_service.initialize(client)
            self.dht_lcd_service.initialize(client)
            self.rgb_ir_service.initialize(client)
        else:
            logger.exception("MQTT connect failed:", reason_code)
