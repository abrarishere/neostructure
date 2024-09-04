import os

import pkg_resources  # For accessing package resources

from neostructure.markdowns.enhancements.refine_json import refine_json
from neostructure.markdowns.fetch import convert_markdown_to_json, get_links, get_readme
from neostructure.setup_nvim.create_structure import create_structure
from neostructure.show import main


# Use pkg_resources to access files within the package
def get_resource_path(resource_name):
    return pkg_resources.resource_filename(__name__, resource_name)


FILE_NAME = get_resource_path("markdowns/README.md")
LINKS_FILE = get_resource_path("markdowns/mds/links.md")
JSON_FILE = get_resource_path("markdowns/jsons/links.json")
SELECTED_PLUGINS_FILE = get_resource_path("markdowns/jsons/selected_plugins.json")
ENHANCEMENTS_FILE = get_resource_path("markdowns/jsons/enhancements.json")


def app():
    # Use os.path.join for paths within the package
    mds_path = os.path.join(os.path.dirname(FILE_NAME), "mds")
    jsons_path = os.path.join(os.path.dirname(FILE_NAME), "jsons")

    # Make sure to handle paths correctly within the package
    if os.path.exists(mds_path):
        os.system(f"rm -r {mds_path}")
    if os.path.exists(jsons_path):
        os.system(f"rm -r {jsons_path}")

    os.makedirs(mds_path, exist_ok=True)
    os.makedirs(jsons_path, exist_ok=True)

    get_readme(FILE_NAME)
    get_links(FILE_NAME, LINKS_FILE)
    convert_markdown_to_json(LINKS_FILE, JSON_FILE)
    refine_json(JSON_FILE, ENHANCEMENTS_FILE)
    main(ENHANCEMENTS_FILE, SELECTED_PLUGINS_FILE)
    create_structure(SELECTED_PLUGINS_FILE)


if __name__ == "__main__":
    app()
