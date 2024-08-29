import json
import re
from urllib.parse import urlparse


def extract_repo_from_url(url):
    """Extract the repository part from a URL."""
    parsed_url = urlparse(url)
    path = parsed_url.path.strip("/").split("/")
    if len(path) >= 2:
        return f"{path[0]}/{path[1]}"
    return url


def refine_json(input_file, output_file):
    """Refine JSON file by removing categories with no plugins and cleaning category names."""
    try:
        with open(input_file, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file: {e}")
        return

    refined_data = {}
    for category, plugins in data.items():
        # Remove the '#' symbol from category names
        clean_category = category.lstrip("#").strip()
        if plugins:
            refined_data[clean_category] = []

            for plugin in plugins:
                # Remove the text after '#' in plugin names
                plugin_name = plugin["name"].split("#")[0].strip()

                # Use URL to correct plugin name if it does not contain '/'
                if "/" not in plugin_name and "url" in plugin:
                    plugin_name = extract_repo_from_url(plugin["url"])

                plugin["name"] = plugin_name
                refined_data[clean_category].append(plugin)

    try:
        with open(output_file, "w") as f:
            json.dump(refined_data, f, indent=4)
            print(f"Refined JSON file saved to {output_file}")
    except IOError as e:
        print(f"Error saving file: {e}")
