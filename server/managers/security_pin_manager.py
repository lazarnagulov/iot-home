from time import time

import config.settings as settings
import config.extensions as extensions
from services.alarm_service import AlarmService

class SecurityPinManager:
    def __init__(self, alarm_service: AlarmService):
        self.pin_queue = []
        self.last_press_time = time()
        self._alarm_service = alarm_service

    def handle_key(self, key):
        current_time = time()
        if current_time - self.last_press_time > 10:
            self.pin_queue.clear()
        self.last_press_time = current_time

        self.pin_queue.append(key)
        if len(self.pin_queue) > 5:
            self.pin_queue.pop(0)
        if len(self.pin_queue) != 5 or self.pin_queue[-1] != "#":
            return

        pin = "".join(self.pin_queue[:-1])
        if pin == settings.Config.SECURITY_PIN:
            self.pin_queue.clear()
            print("Valid PIN entered, toggling alarm state")
            self._alarm_service.swap_state()