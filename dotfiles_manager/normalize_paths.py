#!/usr/bin/env python3
"""Normalize paths in dotfiles.json to use $HOME variable."""

import os
import re
from .config import load_or_create_config, save_config

def normalize_home_paths():
    """Replace hardcoded home directory paths with $HOME variable."""
    config = load_or_create_config()
    
    # Get the current user's home directory
    home_dir = os.path.expanduser("~")
    
    changes_made = False
    
    if "dotfiles" in config:
        for name, dotfile_config in config["dotfiles"].items():
            if "destination" in dotfile_config:
                dest = dotfile_config["destination"]
                
                # Replace hardcoded home directory with $HOME
                if dest.startswith(home_dir):
                    new_dest = dest.replace(home_dir, "$HOME", 1)
                    if new_dest != dest:
                        dotfile_config["destination"] = new_dest
                        print(f"Updated {name}: {dest} -> {new_dest}")
                        changes_made = True
    
    if changes_made:
        save_config(config)
        print("Path normalization complete!")
    else:
        print("No paths needed normalization.")

if __name__ == "__main__":
    normalize_home_paths()
