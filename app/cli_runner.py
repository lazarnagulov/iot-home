import logging
import threading
import time

from app.cli.console import run_actuator_cli
from app.system_manager import SystemManager
from config import Config, load_config

logger = logging.getLogger("iot_home")


def run_cli_mode(simulated: bool = False) -> None:
    logger.info("Starting IoT Home in CLI mode")
    
    config = load_config()
    manager = SystemManager(config)
    
    try:
        manager.initialize()
        
        console_thread = threading.Thread(
            target=run_actuator_cli,
            args=(manager.registry, manager.stop_event),
            daemon=True
        )
        console_thread.start()
        manager.threads.append(console_thread)
        
        logger.info("System running. Press Ctrl+C to exit or type 'exit' in console.")
        
        while not manager.stop_event.is_set():
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Error in CLI mode: {e}", exc_info=True)
    finally:
        manager.shutdown()