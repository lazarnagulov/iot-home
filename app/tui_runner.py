import logging

from app.app_state import AppState
from app.system_manager import SystemManager
from app.tui.iot_home import IotHomeApp
from config import load_config
from util.logger import get_tui_handler

logger = logging.getLogger("iot_home")


def run_tui_mode(simulated: bool = False) -> None:
    logger.info("Starting IoT Home in TUI mode")
    
    config = load_config()
    manager = SystemManager(config)
    state = AppState()
    
    try:
        manager.initialize()
        
        state.actuator_registry = manager.registry
        state.sensors = {
            "DS1": {"pressed": False},
            "DHT1": {"temp": 0.0, "humidity": 0.0},
            "PIR1": {"motion": False},
        }
        
        tui_handler = get_tui_handler()
        if not tui_handler:
            logger.warning("TUI handler not initialized properly")
        
        app = IotHomeApp(state)
        app.run()
        
    except Exception as e:
        logger.error(f"Error in TUI mode: {e}", exc_info=True)
    finally:
        manager.shutdown()