import json


def refine_json(input_file, output_file):
    """Refine JSON file by removing categories with no plugins and cleaning category names."""
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file: {e}")
        return

    refined_data = {}
    for category, plugins in data.items():
        # Remove the '#' symbol from category names
        clean_category = category.lstrip('#').strip()
        if plugins:
            refined_data[clean_category] = plugins

    try:
        with open(output_file, 'w') as f:
            json.dump(refined_data, f, indent=4)
            print(f"Refined JSON file saved to {output_file}")
    except IOError as e:
        print(f"Error saving file: {e}")

