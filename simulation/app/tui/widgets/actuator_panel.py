from typing import Dict
from textual.reactive import reactive
from rich.text import Text
from textual.widgets import Static

from actuators.actuator_registry import Actuator


class ActuatorPanel(Static):
    actuators: Dict[str, Actuator] = reactive({}, always_update=True)  # ty: ignore[invalid-assignment]

    def update_from_state(self, actuators: Dict[str, Actuator]) -> None:
        if self.is_mounted:
            self.actuators = dict(actuators)

    def watch_actuators(self, actuators: Dict[str, Actuator]) -> None:
        self.update(self._render_actuators(actuators))

    def _render_actuators(self, actuators: Dict[str, Actuator]) -> Text:
        text = Text()

        if not actuators:
            text.append("No actuators registered", style="dim italic")
            return text

        max_name_len = max((len(name) for name in actuators.keys()), default=0)

        for name, actuator in actuators.items():
            state = actuator.state
            active = state.is_active()
            
            indicator = "■" if active else "□"
            indicator_style = "green" if active else "dim"
            text.append(indicator, style=indicator_style)
            text.append("  ")

            text.append(name.ljust(max_name_len), style="bold")
            text.append("  ")

            state_str = str(state)
            state_style = "green" if active else "dim"
            if '\n' in state_str:
                state_str = state_str.replace("\n", "\n" + " " * (max_name_len + 6))
            text.append(state_str, style=state_style)

            text.append("\n")

        return text