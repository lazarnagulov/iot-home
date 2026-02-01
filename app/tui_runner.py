import logging

from app.system_manager import SystemManager
from app.tui.iot_home import IotHomeApp
from config import load_config
from util.logger import get_tui_handler

logger = logging.getLogger("iot_home")


def run_tui_mode(config_path: str) -> None:
    logger.info("Starting IoT Home in TUI mode")
    
    config = load_config(config_path)
    manager = SystemManager(config)
    
    try:
        manager.initialize()
        
        manager.state.sensors = {
            "DS1": {"pressed": False},
            "DUS1": {"distance": 0.0},
            "DPIR1": {"motion": False},
            "DMS": {"last_key": "None"},
        }
        
        tui_handler = get_tui_handler()
        if not tui_handler:
            logger.warning("TUI handler not initialized properly")
        
        app = IotHomeApp(manager.state, manager.event_bus)
        app.run()
        
    except Exception as e:
        logger.error(f"Error in TUI mode: {e}", exc_info=True)
    finally:
        manager.shutdown()