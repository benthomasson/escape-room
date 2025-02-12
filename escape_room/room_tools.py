from smolagents.tools import Tool
from escape_room.local_python_executor import FinalAnswerException
from .tools import get_json_schema


class OpenDoor(Tool):
    name = "open_door"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str) -> bool:
        """Opens the door with the given name. Returns True if successful, False otherwise.

        Args:
            name: The name of the door to open.

        Returns:
            boolean
        """
        if name == "exit":
            if self.state["LOCKED"]:
                raise Exception("Locked. Look for a key.")
            raise FinalAnswerException("Success!")
        else:
            raise Exception(f"there is no door named {name}")

    description, inputs, output_type = get_json_schema(forward)


class UnlockDoor(Tool):
    name = "unlock_door"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, using: str) -> bool:
        """Unlocks the door with the given name and given item. Returns True if successful, False otherwise.

        Args:
            name: The name of the door to unlock.
            using: The name of the item to unlock the door with.

        Returns:
            boolean
        """
        if name == "exit" and using == "pick":
            self.state["LOCKED"] = False
            return True
        elif name != "exit":
            raise Exception(f"there is no door named {name}")
        elif using != "pick":
            raise Exception(f"{name} is the wrong key")
        raise Exception("wat")

    description, inputs, output_type = get_json_schema(forward)


class OpenChest(Tool):
    name = "open_chest"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str) -> list[str]:
        """Opens the chest with the given name. Returns the contents of the chest as a list

        Args:
            name: The name of the door to open.

        Returns:
            array
        """

        return ["pick"]

    description, inputs, output_type = get_json_schema(forward)


class LookAround(Tool):
    name = "look_around"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self) -> list[str]:
        """
        Shows you what is in the room with you.

        Returns:
            array
        """

        return ["exit", "chest"]

    description, inputs, output_type = get_json_schema(forward)


TOOLS = {
    "open_door": OpenDoor,
    "open_chest": OpenChest,
    "unlock_door": UnlockDoor,
    "look_around": LookAround,
}


def get_tool(state, name):
    return TOOLS[name](state)
