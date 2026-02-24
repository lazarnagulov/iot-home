import math

from services.alarm_service import AlarmService, AlarmState
import config.settings as settings

class GyroManager:
    def __init__(self, alarm_service: AlarmService):
        self._alarm_service = alarm_service
        self._violation_count = 0
        self.REQUIRED_VIOLATIONS = 2

    def handle_gyro_state(self, value):
        gx = value.get("gyro_x", 0)
        gy = value.get("gyro_y", 0)
        gz = value.get("gyro_z", 0)
        print(f"Gyro: {gx}, {gy}, {gz}")
        
        magnitude = math.sqrt(gx**2 + gy**2 + gz**2)
        print(f"Magnitude: {magnitude}")

        if magnitude > settings.Config.GYROSCOPE_THRESHOLD:
            print(f"Significant motion detected - magnitude: {magnitude}")
            self._violation_count += 1
            if self._violation_count >= self.REQUIRED_VIOLATIONS:
                self._alarm_service.trigger()
        else:
            self._violation_count = 0
    
    def on_alarm_state_changed(self, new_state: AlarmState) -> None:
        if new_state == AlarmState.DISARMED:
            self._violation_count = 0