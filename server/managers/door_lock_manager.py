import threading
from typing import Optional
from enum import Enum

import config.settings as settings
import config.extensions as extensions
from services.alarm_service import AlarmState, AlarmService

class DoorLockManager:
    def __init__(self, alarm_service: AlarmService):
        self._alarm_service = alarm_service
        self.is_unlocked = False

        self._left_unlocked_timer: Optional[threading.Timer] = None
        self._breach_timer: Optional[threading.Timer] = None
        self._left_unlocked_triggered_alarm = False

    def handle_lock_state(self, unlocked: bool):
        """ Pressed button = door unlocked, released button = door locked """
        if unlocked == self.is_unlocked: # State unchanged
            return
        
        self.is_unlocked = unlocked

        if unlocked:
            self._on_door_unlocked()
        else:
            self._on_door_locked()

    def _on_door_unlocked(self):
        alarm_state = self._alarm_service.alarm_state
        if alarm_state == AlarmState.ARMED:
            self._start_breach_timer()
        elif alarm_state == AlarmState.DISARMED:
            self._start_left_unlocked_timer()

    def _on_door_locked(self):
        alarm_state = self._alarm_service.alarm_state    
        self._cancel_left_unlocked_timer()
        if alarm_state == AlarmState.TRIGGERED and self._left_unlocked_triggered_alarm:
            self._alarm_service.disarm()

    def on_alarm_state_changed(self, new_state: AlarmState):
        if new_state == AlarmState.DISARMED:
            self._cancel_breach_timer()
            self._cancel_left_unlocked_timer()
            self._left_unlocked_triggered_alarm = False

    def _trigger_breach_alarm(self):
        print("Door breached, triggering alarm")
        self._alarm_service.trigger(force=True)

    def _trigger_left_unlocked_alarm(self):
        print("Door left unlocked, triggering alarm")
        self._left_unlocked_triggered_alarm = True
        self._alarm_service.trigger(force=True)

    def _start_breach_timer(self):
        if self._breach_timer is not None:
            self._breach_timer.cancel()
        self._breach_timer = threading.Timer(settings.Config.UNLOCK_ALARM_LEEWAY, self._trigger_breach_alarm)
        self._breach_timer.start()

    def _cancel_breach_timer(self):
        if self._breach_timer is not None:
            self._breach_timer.cancel()
            self._breach_timer = None

    def _start_left_unlocked_timer(self):
        if self._left_unlocked_timer is not None:
            self._left_unlocked_timer.cancel()
        self._left_unlocked_timer = threading.Timer(settings.Config.DOOR_LEFT_UNLOCKED_TIME_THRESHOLD, self._trigger_left_unlocked_alarm)
        self._left_unlocked_timer.start()

    def _cancel_left_unlocked_timer(self):
        if self._left_unlocked_timer is not None:
            self._left_unlocked_timer.cancel()
            self._left_unlocked_timer = None