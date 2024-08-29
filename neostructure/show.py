import json

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

console = Console()

def load_data(file):
    """Load JSON data from a file."""
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        console.print(f"[red]Error loading file: {e}[/red]", style="bold red")
        exit()

def show_categories(data):
    """Display categories as a tree and allow user to select one."""
    tree = Tree("Categories", style="bold green")
    categories = list(data.keys())
    for category in categories:
        tree.add(category)
    
    console.print(tree)
    while True:
        category = Prompt.ask("Select a category by name (or type 'q' to quit):").strip()
        if category == 'q':
            console.print("Exiting the program.", style="bold red")
            exit()
        elif category in data:
            return category
        else:
            console.print(f"[red]Invalid category '{category}'. Please try again.[/red]", style="bold red")

def show_plugins(data, category):
    """Display plugins for a selected category and allow user to select them."""
    plugins = data.get(category, [])
    if not plugins:
        console.print("[yellow]No plugins available in this category.[/yellow]", style="bold yellow")
        return []

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Select", style="dim", width=6)
    table.add_column("Name", style="dim")
    table.add_column("URL")
    table.add_column("Description")

    plugin_names = []
    for idx, plugin in enumerate(plugins):
        name = plugin.get('name', 'Unknown')
        url = plugin.get('url', 'No URL')
        description = plugin.get('description', 'No Description')
        table.add_row(f"[green]{idx + 1}[/green]", name, url, description)
        plugin_names.append(name)

    console.print(Panel(table, title=f"Plugins in {category}", title_align="left"))

    while True:
        selected_indices = Prompt.ask(
            "Enter the numbers of plugins you want to select (comma-separated), or type 'q' to quit:"
        ).strip()
        if selected_indices.lower() == 'q':
            exit()
        try:
            selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(',')]
            if all(0 <= idx < len(plugin_names) for idx in selected_indices):
                return [plugin_names[idx] for idx in selected_indices]
            else:
                console.print("[red]Invalid selection. Please enter valid numbers.[/red]", style="bold red")
        except ValueError:
            console.print("[red]Invalid input. Please enter numbers separated by commas.[/red]", style="bold red")

def save_selection(data, selected_plugins, output_file):
    """Save the selected plugins to a JSON file."""
    selected_data = []
    for plugin_name in selected_plugins:
        for category in data:
            for item in data[category]:
                if item.get('name') == plugin_name:
                    selected_data.append({
                        'name': plugin_name,
                        'url': item.get('url'),
                        'category': category
                    })
                    break

    try:
        with open(output_file, 'w') as f:
            json.dump(selected_data, f, indent=4)
        console.print(f"[green]Selected plugins saved to {output_file}[/green]", style="bold green")
    except IOError as e:
        console.print(f"[red]Error saving file: {e}[/red]", style="bold red")

def main(input_file, output_file):
    data = load_data(input_file)
    selected_plugins = []

    while True:
        category = show_categories(data)
        console.print(f"\nDisplaying plugins for category: {category}\n")
        
        plugin_names = show_plugins(data, category)
        if not plugin_names:
            continue
        
        selected_plugins.extend(plugin_names)

        if Prompt.ask("Do you want to select plugins from another category? (y/n):").strip().lower() != 'y':
            if selected_plugins:
                    save_selection(data, selected_plugins,  output_file)
            console.print("[bold cyan]Thank you for using the plugin customizer![/bold cyan]")
            break

