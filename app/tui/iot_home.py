from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Input

from app.app_state import AppState
from app.tui.widgets.actuator_panel import ActuatorPanel
from app.tui.widgets.sensor_panel import SensorPanel
from util.command_handler import handle_command

class IotHomeApp(App):

    CSS = """
    Screen {
        layout: vertical;
    }

    #main {
        height: 1fr;
        layout: horizontal;
    }

    #sensors {
        width: 3fr;
        border: round green;
        padding: 1;
    }

    #actuators {
        width: 2fr;
        border: round blue;
        padding: 1;
    }

    Input {
        dock: bottom;
    }
    """

    def __init__(self, state: AppState):
        super().__init__()
        self.state: AppState = state

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="main"):
            yield SensorPanel(id="sensors")
            yield ActuatorPanel(id="actuators")

        self.command_input = Input(
            placeholder="Type command"
        )
        yield self.command_input

        yield Footer()

    def on_mount(self) -> None:
        self.actuator_panel = self.query_one("#actuators", ActuatorPanel)
        self.sensor_panel = self.query_one("#sensors", SensorPanel)
        self.set_interval(0.5, self.refresh_ui)

    def refresh_ui(self) -> None:
        self.actuator_panel.update_from_state(self.state.actuator_registry.get_all())
        self.sensor_panel.update_from_state(self.state.sensors)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value.strip().lower()
        result = handle_command(cmd, self.state.actuator_registry)
        self.command_input.value = ""
        
        if result == "EXIT":
            self.exit()