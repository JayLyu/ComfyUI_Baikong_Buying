blue = "\033[34m"
green = "\033[92m"
color_end = "\033[0m"

from .node_mappings import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# WEB_DIRECTORY = "./web"

print(f"{blue}ComfyUI Baikong Buying: {green}Loaded nodes successfully.{color_end}")

# __all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]