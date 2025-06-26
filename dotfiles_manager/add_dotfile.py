#!/usr/bin/env python3
"""Add dotfile functionality for dotfiles manager."""

import os
from .config import load_or_create_config, save_config

def add_dotfile(name, source, dest, file_type=None):
    """Add new dotfile configuration."""
    config = load_or_create_config()
    
    if "dotfiles" not in config:
        config["dotfiles"] = {}
    
    # Auto-detect type if not specified
    if file_type is None:
        source_expanded = os.path.expandvars(source)
        if os.path.exists(source_expanded):
            file_type = "directory" if os.path.isdir(source_expanded) else "file"
        else:
            file_type = "file"  # Default to file if source doesn't exist
    
    config["dotfiles"][name] = {
        "type": file_type,
        "source": source, 
        "destination": dest
    }
    save_config(config)
    print(f"Added: {name} (type: {file_type})")
