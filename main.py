import asyncio

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

import logging

# Set the logging level for  semantic_kernel.kernel to DEBUG.
logging.basicConfig(
    format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("kernel").setLevel(logging.DEBUG)

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



async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completion
    chat_completion = AzureChatCompletion(
        env_file_path=".env",
    )
    kernel.add_service(chat_completion)

    # Set the logging level for  semantic_kernel.kernel to DEBUG.
    setup_logging()
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Add a plugin (the LightsPlugin class is defined below)
    kernel.add_plugin(
        LightsPlugin(),
        plugin_name="Lights",
    )

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create a history of the conversation
    history = ChatHistory()

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit" or userInput == "quit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        # Get the response from the AI
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())