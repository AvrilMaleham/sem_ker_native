from semantic_kernel.functions import kernel_function

class ThermostatPlugin:
    def __init__(self):
        self.current_temp = 22  # default temperature in °C
        self.target_temp = 22
        self.mode = "auto"  # other options: "heat", "cool", "off"

    @kernel_function(
        name="get_temperature",
        description="Returns the current and target temperatures.",
    )
    def get_temperature(self) -> str:
        return f"The current temperature is {self.current_temp}°C, target is {self.target_temp}°C, mode is '{self.mode}'."

    @kernel_function(
        name="set_temperature",
        description="Sets the target temperature.",
    )
    def set_temperature(self, temp: float) -> str:
        self.target_temp = temp
        return f"Target temperature set to {temp}°C."

    @kernel_function(
        name="increase_temperature",
        description="Increases the target temperature by 1°C.",
    )
    def increase_temperature(self) -> str:
        self.target_temp += 1
        return f"Target temperature increased to {self.target_temp}°C."

    @kernel_function(
        name="decrease_temperature",
        description="Decreases the target temperature by 1°C.",
    )
    def decrease_temperature(self) -> str:
        self.target_temp -= 1
        return f"Target temperature decreased to {self.target_temp}°C."

    @kernel_function(
        name="set_mode",
        description="Sets the mode of the thermostat to 'heat', 'cool', 'auto', or 'off'.",
    )
    def set_mode(self, mode: str) -> str:
        if mode.lower() in ["heat", "cool", "auto", "off"]:
            self.mode = mode.lower()
            return f"Thermostat mode set to '{self.mode}'."
        return f"Invalid mode '{mode}'. Please choose from 'heat', 'cool', 'auto', or 'off'."
