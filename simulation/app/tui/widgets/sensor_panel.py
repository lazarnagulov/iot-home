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
        
        for sensor_idx, (id, values) in enumerate(self.sensors.items()):
            name = values.get("name", id)
            values = values.get("value", {})
            text.append(f"{name}", style="bold cyan")
            text.append("\n")
            
            for key, value in values.items():
                key_text = f"  {key:15} "
                text.append(key_text, style="dim")

                if isinstance(value, bool):
                    style = "green" if value else "red"
                    text.append(str(value).upper(), style=style)
                elif isinstance(value, (int, float)):
                    text.append(str(value), style="magenta")
                elif isinstance(value, str):
                    if '\n' in value:
                        value = value.replace("\n", "\n" + " " * (len(key_text)))
                    text.append(value, style="white")
                else:
                    text.append(str(value), style="white")

                text.append("\n")
            
            if sensor_idx < len(self.sensors) - 1:
                text.append("\n")

        return text