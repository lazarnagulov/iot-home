from typing import Any, Dict
from textual.widget import Widget
from textual.app import RenderResult
from textual.reactive import reactive
from rich.text import Text


class SensorPanel(Widget):
    sensors: Dict[str, Any] = reactive({}, always_update=True) # ty: ignore[invalid-assignment]
    
    def update_from_state(self, sensors: Dict[str, Any]) -> None:
        self.sensors = dict(sensors)
    
    def render(self) -> RenderResult:
        text = Text()
        
        if not self.sensors:
            text.append("No sensor data available", style="dim italic")
            return text
        
        for sensor_idx, (name, values) in enumerate(self.sensors.items()):
            text.append(f"{name}", style="bold cyan")
            text.append("\n")
            
            for key, value in values.items():
                text.append(f"  {key:15} ", style="dim")

                if isinstance(value, bool):
                    style = "green" if value else "red"
                    text.append(str(value).upper(), style=style)
                elif isinstance(value, (int, float)):
                    text.append(str(value), style="magenta")
                else:
                    text.append(str(value), style="white")

                text.append("\n")
            
            if sensor_idx < len(self.sensors) - 1:
                text.append("\n")

        return text