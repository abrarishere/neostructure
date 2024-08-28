import os

from markdowns.enhancements.refine_json import refine_json
from markdowns.fetch import convert_markdown_to_json, get_links, get_readme
from setup_nvim.create_structure import create_structure
from show import main

FILE_NAME = os.path.join(os.path.dirname(__file__), 'markdowns/README.md')
LINKS_FILE = os.path.join(os.path.dirname(__file__), 'markdowns/mds/links.md')
JSON_FILE = os.path.join(os.path.dirname(__file__), 'markdowns/jsons/links.json')
SELECTED_PLUGINS_FILE = os.path.join(os.path.dirname(__file__), 'markdowns/jsons/selected_plugins.json')
PATH = os.path.dirname(os.path.abspath(__file__))

def app():
    os.system(f'rm -r {PATH}/markdowns/mds')
    os.system(f'rm -r {PATH}/markdowns/jsons')
    os.system(f'mkdir {PATH}/markdowns/mds')
    os.system(f'mkdir {PATH}/markdowns/jsons')
    get_readme(FILE_NAME)
    get_links(FILE_NAME, LINKS_FILE)
    convert_markdown_to_json(LINKS_FILE, JSON_FILE)
    refine_json(JSON_FILE, JSON_FILE)
    main(JSON_FILE, SELECTED_PLUGINS_FILE)
    create_structure(SELECTED_PLUGINS_FILE)

if __name__ == '__main__':
    app()
