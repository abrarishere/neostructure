import json
import re

import requests

# url : https://github.com/rockerBOO/awesome-neovim

def get_readme(file):
    url = "https://raw.githubusercontent.com/rockerBOO/awesome-neovim/master/README.md"
    response = requests.get(url)
    with open(file, "w") as f:
        f.write(response.text)

def get_links(file, outputfile):
    with open(file, "r") as f:
        lines = f.readlines()
    with open(outputfile, "w") as f:
        for line in lines:
            if line.startswith("- [") or line.startswith("## ") or line.startswith("### "):
                f.write(line)
        



def convert_markdown_to_json(input_file, output_file):
    data = {}
    category = None

    with open(input_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("## "):
            # Update the category
            category = line[3:].strip()
            data[category] = []
        elif line.startswith("- "):
            # Parse the plugin details
            match = re.match(r'- \[([^\]]+)\]\(([^)]+)\) - (.+)', line)
            if match:
                name, url, description = match.groups()
                plugin = {
                    "name": name.strip(),
                    "url": url.strip(),
                    "description": description.strip()
                }
                if category:
                    data[category].append(plugin)

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

