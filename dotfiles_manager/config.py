#!/usr/bin/env python3
"""Configuration management for dotfiles manager."""

import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dotfiles.json")

def load_or_create_config():
    """Load config or create default one."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            print(f"Error reading {CONFIG_FILE}, creating new one")
    
    # Create default config
    config = {
        "dotfiles": {
            "_vimrc": {"type": "file", "source": "./.files/.vimrc", "destination": "$HOME/.vimrc"},
            ".tmux.conf": {"type": "file", "source": "./.files/.tmux.conf", "destination": "$HOME/.tmux.conf"},
            ".bashfuncs": {"type": "directory", "source": "./.bashfuncs", "destination": "$HOME/.bashfuncs"}
        }
    }
    
    save_config(config)
    return config

def save_config(config):
    """Save config to JSON file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Config saved to {CONFIG_FILE}")
    except Exception as e:
        print(f"Error saving config: {e}")
