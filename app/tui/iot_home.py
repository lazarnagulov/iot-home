from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Input

from app.app_state import AppState
from app.tui.widgets.actuator_panel import ActuatorPanel
from app.tui.widgets.sensor_panel import SensorPanel
from app.tui.widgets.log_panel import LogPanel
from util.command_handler import handle_command
from util.logger import get_tui_handler


class IotHomeApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }

    #main {
        height: 2fr;
        layout: horizontal;
        padding: 1 2 0 2;
    }

    #sensors {
        width: 3fr;
        border: solid green;
        padding: 1 2;
        margin-right: 1;
    }

    #actuators {
        width: 2fr;
        border: solid blue;
        padding: 1 2;
    }

    #logs {
        height: 1fr;
        border: solid yellow;
        padding: 1 2;
        margin: 0 2;
    }

    Input {
        dock: bottom;
        margin: 0 2 1 2;
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

        yield LogPanel(id="logs", max_lines=50)

        self.command_input = Input(
            placeholder="Enter command..."
        )
        yield self.command_input

        yield Footer()

    def on_mount(self) -> None:
        self.title = "IoT Home Control"
        
        self.actuator_panel = self.query_one("#actuators", ActuatorPanel)
        self.sensor_panel = self.query_one("#sensors", SensorPanel)
        self.log_panel = self.query_one("#logs", LogPanel)
        
        self.actuator_panel.border_title = "Actuators"
        self.sensor_panel.border_title = "Sensors"
        self.log_panel.border_title = "Activity Log"
        
        tui_handler = get_tui_handler()
        if tui_handler:
            tui_handler.set_log_panel(self.log_panel)
        
        self.actuator_panel.update_from_state(
           self.state.actuator_registry.get_all()
        )

        self.sensor_panel.update_from_state(
           self.state.sensors
        )
        
        self.command_input.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value.strip().lower()
        
        if not cmd:
            return
            
        result = handle_command(cmd, self.state.actuator_registry)
        self.command_input.value = ""
        self.actuator_panel.update_from_state(
            self.state.actuator_registry.get_all()
        )

        if result == "EXIT":
            self.exit()