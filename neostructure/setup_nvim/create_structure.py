import json
import os
import shutil

from rich.console import Console

from neostructure.setup_nvim.get_opts import (
    get_dependencies,
    is_plugin_present,
    is_require_setup,
)

console = Console()


def create_directories(base_dir, selected_colorscheme=None):
    """Create the necessary directory structure for the Nvim configuration."""
    nvim_dir = os.path.join(base_dir, "nvim")
    lua_dir = os.path.join(nvim_dir, "lua")
    plugins_dir = os.path.join(lua_dir, "plugins")

    os.makedirs(plugins_dir, exist_ok=True)

    init_lua_content = """-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\\n", "ErrorMsg" },
      { out, "WarningMsg" },
      { "\\nPress any key to exit..." },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end
vim.opt.rtp:prepend(lazypath)

-- Setup mapleader and maplocalleader
vim.g.mapleader = " "

-- Setup lazy.nvim
require("lazy").setup({
  spec = { { import = "plugins" } },
  install = {},
  checker = { enabled = true },
})
"""

    if selected_colorscheme:
        init_lua_content += (
            f"\n-- Colorscheme setup\nvim.cmd('colorscheme {selected_colorscheme}')\n"
        )

    with open(os.path.join(nvim_dir, "init.lua"), "w") as f:
        f.write(init_lua_content)


def format_dependencies(deps):
    return "{ " + ", ".join(f"'{dep}'" for dep in deps) + " }" if deps else "{}"


def create_plugin_files(selected_plugins, base_dir):
    """Create the plugins.lua file based on the selected plugins."""
    plugins_dir = os.path.join(base_dir, "nvim", "lua", "plugins")

    plugin_entries = []

    for plugin in selected_plugins:
        deps_lua = format_dependencies(get_dependencies(plugin["name"]))
        opts = is_plugin_present(plugin["name"])
        requires = is_require_setup(plugin["name"])

        entry = f"  {{ '{plugin['name']}', dependencies = {deps_lua}"
        if opts:
            entry += ", opts = {}"
        if requires:
            entry += ", config = function() require('{plugin['name']}') end"
        entry += " }"

        plugin_entries.append(entry)

    plugins_lua_content = "return {\n" + ",\n".join(plugin_entries) + "\n}"
    with open(os.path.join(plugins_dir, "plugins.lua"), "w") as f:
        f.write(plugins_lua_content)


def create_structure(selected_plugins_file):
    """Create the Nvim configuration structure."""
    base_dir = os.path.expanduser(
        f"~/.config/{input('Enter the base directory name for the Nvim configuration: ')}"
    )
    nvim_dir = os.path.join(base_dir, "nvim")

    if os.path.exists(nvim_dir):
        response = input(
            f"{nvim_dir} already exists. Merge or overwrite? (m/o): "
        ).lower()
        if response == "o":
            shutil.rmtree(nvim_dir, ignore_errors=True)
            os.makedirs(nvim_dir)
        elif response != "m":
            console.print("[red]Invalid response. Exiting...[/red]")
            return

    os.makedirs(base_dir, exist_ok=True)
    selected_colorscheme = input(
        "Enter the colorscheme (or press Enter to skip): "
    ).strip()

    create_directories(base_dir, selected_colorscheme)

    try:
        with open(selected_plugins_file, "r") as f:
            selected_plugins = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        console.print(f"[red]Error loading JSON file: {e}[/red]")
        return

    create_plugin_files(selected_plugins, base_dir)

    console.print(f"[green]Nvim configuration has been set up in {base_dir}[/green]")
    console.print(
        "[blue]You can now start Nvim to install the selected plugins.[/blue]"
    )
    console.print(
        "[cyan]Remember to always configure plugins in the plugins.lua file.[/cyan]"
    )
    console.print("[yellow]Happy Vimming![/yellow]")
