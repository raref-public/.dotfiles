#!/usr/bin/env python3
"""Listing functionality for dotfiles manager."""

from .config import load_or_create_config

def list_dotfiles():
    """List all configured dotfiles."""
    config = load_or_create_config()
    
    print("Configured dotfiles:")
    for name, paths in config.get("dotfiles", {}).items():
        file_type = paths.get('type', 'file')
        type_indicator = "📁" if file_type == "directory" else "📄"
        print(f"  {type_indicator} {name} ({file_type}): {paths.get('source')} -> {paths.get('destination')}")
