from time import time
from collections import deque

from services.alarm_service import AlarmService, AlarmState
import config.settings as settings

class PersonCountManager:
    person_count: int
    def __init__(self, alarm_service: AlarmService):
        self._alarm_service = alarm_service
        PersonCountManager.person_count = 0
        self._past_distances = {}
        self._last_distance_times = {}
        self._last_count_change_time = time()
        self._distance_theshold = 10

    def handle_distance(self, sensor_id, distance):
        if sensor_id in self._last_distance_times:
            if time() - self._last_distance_times[sensor_id] > 2:
                self._past_distances[sensor_id].clear()
        self._last_distance_times[sensor_id] = time()
        
        if sensor_id in self._past_distances:
            self._past_distances[sensor_id].append(distance)
        else:
            self._past_distances[sensor_id] = deque(maxlen=4)
            self._past_distances[sensor_id].append(distance)

    def handle_motion(self, sensor_id, distance_sensor_id, motion):
        if motion:
            if distance_sensor_id is not None and distance_sensor_id in self._last_distance_times:
                if time() - self._last_distance_times[distance_sensor_id] > 2:
                    self._past_distances[distance_sensor_id].clear()
            entry_or_exit = self._motion_detected(sensor_id, distance_sensor_id, motion)
            if not entry_or_exit and PersonCountManager.person_count == 0:
                self._alarm_service.trigger()

    def _motion_detected(self, sensor_id, distance_sensor_id, motion) -> bool:
        if distance_sensor_id is None: # Sensor without corresponding distance sensor triggered, can't be entry or exit
            return False
        if time() - self._last_count_change_time < settings.Config.PERSON_COUNT_COOLDOWN:
            return True
        if not distance_sensor_id in self._past_distances:
            return False # We can't conclude movement without distance data
        distances = self._past_distances[distance_sensor_id]
        if len(distances) < 2:
            return False
        if self._is_decreasing(distances):
            PersonCountManager.person_count += 1
            self._last_count_change_time = time()
            return True
        elif self._is_increasing(distances):
            PersonCountManager.person_count -= 1
            if PersonCountManager.person_count < 0:
                PersonCountManager.person_count = 0
            self._last_count_change_time = time()
            return True
        return False
    
    def _is_increasing(self, distances):
        return distances[-1] - distances[0] > self._distance_theshold
    
    def _is_decreasing(self, distances):
        return distances[0] - distances[-1] > self._distance_theshold