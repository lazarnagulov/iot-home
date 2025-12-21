from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text


class ActuatorPanel(Widget):

    data = reactive(dict)

    def update_from_state(self, actuators: dict):
        self.data = actuators

    def render(self):
        text = Text()

        if not self.data:
            text.append("No actuators registered\n", style="dim")
            return text

        for name, actuator in self.data.items():
            state = "ON" if actuator.state else "OFF"
            style = "green" if actuator.state else "red"

            text.append(f"{name:15} ", style="bold")
            text.append(state, style=style)
            text.append("\n")

        return text
