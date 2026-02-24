from typing import Dict
from textual.reactive import reactive
from rich.text import Text
from textual.types import NoActiveAppError
from textual.widgets import Static

from services.alarm_service import AlarmState

class SecurityPanel(Static):
    alarm_state: AlarmState = reactive(AlarmState.DISARMED, always_update=True)

    def update_from_alarm_state(self, alarm_state: AlarmState) -> None:
        try:
            self.alarm_state = alarm_state
        except NoActiveAppError:
            pass

    def watch_alarm_state(self, alarm_state: AlarmState) -> None:
        self.update(self._render_alarm_state(alarm_state))

    def _render_alarm_state(self, alarm_state: AlarmState) -> Text:
        text = Text()

        if alarm_state == AlarmState.DISARMED:
            text.append("Alarm not armed", style="bold")
        elif alarm_state == AlarmState.ARMED:
            text.append("Alarm armed", style="bold yellow")
        elif alarm_state == AlarmState.TRIGGERED:
            text.append("INTRUSION DETECTED", style="bold red")
        text.append("\n")
        return text