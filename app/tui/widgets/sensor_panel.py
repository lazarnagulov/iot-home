from textual.widget import Widget
from textual.app import RenderResult
from textual.reactive import reactive
from rich.text import Text

class SensorPanel(Widget):

    data = reactive(dict)
    
    def update_from_state(self, sensors: dict) -> None:
        self.data = sensors
    
    def render(self) -> RenderResult:
        text = Text()
        
        if not self.data:
            text.append("No sensor data available\n", style="dim")
            return text
        
        for name, values in self.data.items():
            text.append(f"{name}\n", style="bold underline")

            for key, value in values.items():
                text.append(f"  {key:12}: ")

                if isinstance(value, bool):
                    style = "green" if value else "red"
                    text.append(str(value).upper(), style=style)
                else:
                    text.append(str(value))

                text.append("\n")

            text.append("\n")

        return text