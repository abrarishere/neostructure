import json
import os


def create_directories(base_dir):
    """
    Create the necessary directory structure for the Nvim configuration.
    """
    nvim_dir = os.path.join(base_dir, 'nvim')
    lua_dir = os.path.join(nvim_dir, 'lua')
    plugins_dir = os.path.join(lua_dir, 'plugins')
    
    # Create directories
    os.makedirs(plugins_dir, exist_ok=True)
    
    # Create init.lua in the root nvim directory
    init_lua_path = os.path.join(nvim_dir, 'init.lua')
    init_lua_content = '''-- Bootstrap lazy.nvim
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
  spec = {
    -- import your plugins
    { import = "plugins" },
  },
  install = { colorscheme = { "habamax" } },
  checker = { enabled = true },
})
'''
    with open(init_lua_path, 'w') as f:
        f.write(init_lua_content)

def create_plugin_files(selected_plugins, base_dir):
    """Create the plugins.lua file based on the selected plugins."""
    plugins_dir = os.path.join(base_dir, 'nvim', 'lua', 'plugins')
    
    # Prepare plugin list in Lua format
    plugin_entries = [f"  {{ '{plugin['name']}' }}" for plugin in selected_plugins]
    plugins_lua_content = 'return {\n' + ',\n'.join(plugin_entries) + '\n}'
    
    plugins_lua_path = os.path.join(plugins_dir, 'plugins.lua')
    with open(plugins_lua_path, 'w') as f:
        f.write(plugins_lua_content)

def create_structure(selected_plugins_file):
    # Prompt the user for the base directory name
    base_dir = input("Enter the base directory name for the Nvim configuration: ")
    base_dir = os.path.expanduser(f"~/.config/{base_dir}")
    
    # Create the directory structure
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    create_directories(base_dir)
    
    # Read the selected plugins from JSON
    try:
        with open(selected_plugins_file, 'r') as f:
            selected_plugins = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file: {e}")
        return
    
    # Create plugin files
    create_plugin_files(selected_plugins, base_dir)
    print(f"Nvim configuration has been set up in {base_dir}")
    print("You can now start Nvim to install the selected plugins.")
    print("Remember to always configure plugins in the plugins.lua file.")
    print("Happy Vimming!")

# Example usage
# create_structure('selected_plugins.json')
