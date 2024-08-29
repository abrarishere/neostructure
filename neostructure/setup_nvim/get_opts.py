import json
import os

import requests

SAVE_PATH = os.path.join(os.path.dirname(__file__), "./files/json/single_opt.json")
URL = "https://raw.githubusercontent.com/abrarishere/neostructure/main/neostructure/markdowns/awesome-neovim.md"


def get_file():
    # Create directories and empty file
    with open(SAVE_PATH, "w") as f:
        f.write("")
    # Get the file content
    response = requests.get(URL)
    with open(SAVE_PATH, "w") as f:
        f.write(response.text)


def is_plugin_present(plugin_name):
    with open(SAVE_PATH, "r") as f:
        data = json.load(f)
        if plugin_name in data:
            return data[plugin_name]["opts"]["empty"]


def get_dependencies(plugin_name):
    with open(SAVE_PATH, "r") as f:
        data = json.load(f)
        return data[plugin_name]["dependencies"]


def is_require_setup(plugin_name):
    with open(SAVE_PATH, "r") as f:
        data = json.load(f)
        return data[plugin_name]["require"]


def add_plugin(plugin_name):
    with open(SAVE_PATH, "r") as f:
        data = json.load(f)
        data[plugin_name] = {"opts": {"empty": True}}
