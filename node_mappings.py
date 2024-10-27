import importlib

# define colors
blue = "\033[34m"
green = "\033[92m"
color_end = "\033[0m"

node_module_mappings = {
    'node_housing_decision': 'BK_HousingDecision',
    'node_table_preview': 'BK_Table_Preview',
    'node_district_info': 'BK_District_Info'
}

imported_classes = {}

for module_name, class_name in node_module_mappings.items():
    try:
        module = importlib.import_module(f'.nodes.{module_name}', package=__package__)
        imported_class = getattr(module, class_name)
        imported_classes[class_name] = imported_class
    except ImportError as e:
        print(f"{blue}ComfyUI Node:{green} Import {module_name} failed: {str(e)}{color_end}")
    except AttributeError:
        print(f"{blue}ComfyUI Node:{green} On {module_name} cannot find {class_name}{color_end}")


NODE_CLASS_MAPPINGS = {class_name: imported_classes.get(class_name) for class_name in node_module_mappings.values()}


NODE_DISPLAY_NAME_MAPPINGS = {
    "BK_HousingDecision": "BK Housing Decision",
    "BK_Table_Preview": "BK Table Preview",
    "BK_District_Info": "BK District Info"
}