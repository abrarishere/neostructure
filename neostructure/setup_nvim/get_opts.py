import json
import os

SAVE_PATH = os.path.join(os.path.dirname(__file__), "./files/json/single_opt.json")


def load_data():
    with open(SAVE_PATH, "r") as f:
        return json.load(f)


def is_plugin_present(plugin_name):
    try:
        data = load_data()
        if plugin_name in data:
            return data[plugin_name].get("opts", {}).get("empty", False)
        return False
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[red]Error reading data: {e}[/red]")
        return False


def get_dependencies(plugin_name):
    try:
        data = load_data()
        return data.get(plugin_name, {}).get("dependencies", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[red]Error reading data: {e}[/red]")
        return []


def is_require_setup(plugin_name):
    try:
        data = load_data()
        return data.get(plugin_name, {}).get("require", False)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[red]Error reading data: {e}[/red]")
        return False
