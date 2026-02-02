import logging
import threading
import time

from app.cli.console import run_actuator_cli, run_sensor_cli
from app.system_manager import SystemManager
from config import load_config

logger = logging.getLogger("iot_home")


def run_cli_mode(config_path: str) -> None:
    logger.info("Starting IoT Home in CLI mode")
    
    config = load_config(config_path)
    manager = SystemManager(config)
    
    try:
        manager.initialize()

        console_thread = threading.Thread(
            target=run_actuator_cli,
            args=(manager.state.actuator_registry, manager.stop_event, manager.state),
            daemon=True,
        )
        console_thread.start()
        manager.threads.append(console_thread)

        sensor_thread = threading.Thread(
            target=run_sensor_cli,
            args=(manager.event_bus, manager.state, manager.stop_event),
            daemon=True,
        )
        sensor_thread.start()
        manager.threads.append(sensor_thread)
        
        logger.info("System running. Press Ctrl+C to exit or type 'exit' in console.")
        
        while not manager.stop_event.is_set():
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Error in CLI mode: {e}", exc_info=True)
    finally:
        manager.shutdown()