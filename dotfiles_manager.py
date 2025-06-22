#!/usr/bin/env python3
"""Simple dotfiles manager with diff checking."""

import json
import os
import subprocess
import sys

CONFIG_FILE = "./dotfiles.json"

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
            "_vimrc": {"source": "./_vimrc", "destination": "$HOME/.vimrc"},
            ".tmux.conf": {"source": "./.tmux.conf", "destination": "$HOME/.tmux.conf"},
            ".bashfuncs": {"source": "./.bashfuncs", "destination": "$HOME/.bashfuncs"}
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

def diff_files(source, destination):
    """Compare two files using diff command."""
    source = os.path.expandvars(source)
    destination = os.path.expandvars(destination)
    
    if not os.path.exists(source):
        return f"Source missing: {source}"
    
    if not os.path.exists(destination):
        return f"Destination missing: {destination}"
    
    try:
        result = subprocess.run(["diff", "-u", source, destination], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return "Files identical"
        else:
            return result.stdout
    except Exception as e:
        return f"Diff error: {e}"

def check_all_diffs():
    """Check diffs for all configured dotfiles."""
    config = load_or_create_config()
    
    for name, paths in config.get("dotfiles", {}).items():
        print(f"\n{name}:")
        source = paths.get("source", "")
        dest = paths.get("destination", "")
        
        if not source or not dest:
            print("  Missing source or destination")
            continue
            
        diff_output = diff_files(source, dest)
        
        if diff_output == "Files identical":
            print("  ✓ Identical")
        elif "missing" in diff_output.lower():
            print(f"  ✗ {diff_output}")
        else:
            print("  ✗ Files differ")
            # Show first few lines of diff
            lines = diff_output.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"    {line}")

def list_dotfiles():
    """List all configured dotfiles."""
    config = load_or_create_config()
    
    print("Configured dotfiles:")
    for name, paths in config.get("dotfiles", {}).items():
        print(f"  {name}: {paths.get('source')} -> {paths.get('destination')}")

def add_dotfile(name, source, dest):
    """Add new dotfile configuration."""
    config = load_or_create_config()
    
    if "dotfiles" not in config:
        config["dotfiles"] = {}
    
    config["dotfiles"][name] = {"source": source, "destination": dest}
    save_config(config)
    print(f"Added: {name}")

def main():
    """Main function."""
    if len(sys.argv) == 1:
        check_all_diffs()
    elif sys.argv[1] == "diff":
        check_all_diffs()
    elif sys.argv[1] == "list":
        list_dotfiles()
    elif sys.argv[1] == "add" and len(sys.argv) == 5:
        add_dotfile(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Usage:")
        print("  python dotfiles_manager.py [diff]  - Check diffs (default)")
        print("  python dotfiles_manager.py list   - List dotfiles")
        print("  python dotfiles_manager.py add <name> <source> <dest>")

if __name__ == "__main__":
    main()
