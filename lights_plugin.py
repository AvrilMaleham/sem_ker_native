from semantic_kernel.functions import kernel_function

class LightsPlugin:
    lights = [
        {"id": 1, "name": "Table Lamp", "is_on": False},
        {"id": 2, "name": "Porch light", "is_on": False},
        {"id": 3, "name": "Chandelier", "is_on": True},
    ]

    @kernel_function(
        name="get_lights",
        description="Gets a list of lights and their current state",
    )
    def get_state(
        self,
    ) -> str:
        """Gets a list of lights and their current state."""
        return self.lights

    @kernel_function(
        name="change_state",
        description="Changes the state of the light",
    )
    def change_state(
        self,
        id: int,
        is_on: bool,
    ) -> str:
        """Changes the state of the light."""
        for light in self.lights:
            if light["id"] == id:
                light["is_on"] = is_on
                return light
        return None
        
    @kernel_function(
        name="change_name",
        description="Changes the name of the light",
    )
    def change_name(
        self,
        id: int,
        old_name: str,
        new_name: str,
    ) -> str:
        """Changes the name of the light. From 'old_name' to 'new_name'."""
        for light in self.lights:
            if light["id"] == id and light["name"] == old_name:
                light["name"] = new_name 
                return f"Light '{old_name}' changed to '{new_name}'"
        return f"No light found with id {id} and name '{old_name}'"
    
    @kernel_function(
        name="add_light",
        description="Adds a new light with a name and on/off state.",
    )
    def add_light(
        self,
        name: str,
        is_on: bool = False,
    ) -> str:
        """Adds a new light to the system."""
        new_id = max([light["id"] for light in self.lights], default=0) + 1
        self.lights.append({"id": new_id, "name": name, "is_on": is_on})
        return f"Light '{name}' added with ID {new_id} and state {'on' if is_on else 'off'}."
    
    @kernel_function(
    name="remove_light",
    description="Removes a light by its ID or name.",
)
    def remove_light(
        self,
        id: int = None,
        name: str = None,
    ) -> str:
        """Removes a light from the list by ID or name."""
        if id is not None:
            for light in self.lights:
                if light["id"] == id:
                    self.lights.remove(light)
                    return f"Light with ID {id} removed."
            return f"No light found with ID {id}."

        if name is not None:
            for light in self.lights:
                if light["name"].lower() == name.lower():
                    self.lights.remove(light)
                    return f"Light '{name}' removed."
            return f"No light found with name '{name}'."

        return "Please provide either an ID or a name to remove a light."