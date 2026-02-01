from typing import Dict
from textual.reactive import reactive
from rich.text import Text
from textual.widgets import Static

from actuators.actuator_registry import Actuator


class ActuatorPanel(Static):
    actuators: Dict[str, Actuator] = reactive({}, always_update=True) # ty: ignore[invalid-assignment]

    def update_from_state(self, actuators: Dict[str, Actuator]) -> None:
        self.actuators = dict(actuators)

    def watch_actuators(self, actuators: Dict[str, Actuator]) -> None:
        self.update(self._render_actuators(actuators))

    def _render_actuators(self, actuators: Dict[str, Actuator]) -> Text:
        text = Text()

        if not actuators:
            text.append("No actuators registered", style="dim italic")
            return text

        for name, actuator in actuators.items():
            indicator = "■" if actuator.state.is_active() else "□"
            indicator_style = "green" if actuator.state.is_active() else "dim"
            text.append(indicator, style=indicator_style)
            
            text.append(f"  {name}", style="bold")
            
            state = "ON" if actuator.state.is_active() else "OFF"
            state_style = "green" if actuator.state.is_active() else "dim"
            spacing = " " * (20 - len(name))
            text.append(f"{spacing}{state}", style=state_style)
            text.append("\n")

        return text