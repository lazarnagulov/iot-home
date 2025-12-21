from typing import Dict
from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text

from actuators.base import Actuator


from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from typing import Dict
from actuators.base import Actuator


class ActuatorPanel(Static):

    actuators: Dict[str, Actuator] = reactive({}, always_update=True)

    def update_from_state(self, actuators: Dict[str, Actuator]) -> None:
        self.actuators = dict(actuators)

    def watch_actuators(self, actuators: Dict[str, Actuator]) -> None:
        self.update(self._render_actuators(actuators))

    def _render_actuators(self, actuators: Dict[str, Actuator]) -> Text:
        text = Text()

        if not actuators:
            text.append("No actuators registered\n", style="dim")
            return text

        for name, actuator in actuators.items():
            state = "ON" if actuator.state else "OFF"
            style = "green" if actuator.state else "red"

            text.append(f"{name:15} ", style="bold")
            text.append(state, style=style)
            text.append("\n")

        return text
