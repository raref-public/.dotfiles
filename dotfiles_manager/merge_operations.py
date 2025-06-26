#!/usr/bin/env python3
"""Merge operations for dotfiles manager."""

import os
import subprocess

def merge_files(source, destination):
    """Merge differences between source and destination using vimdiff."""
    source = os.path.expandvars(source)
    destination = os.path.expandvars(destination)
    
    try:
        # Use vimdiff for interactive merging
        print(f"  Opening vimdiff to merge {source} and {destination}")
        print("  Use :wq to save and quit, :q! to quit without saving")
        result = subprocess.run(["vimdiff", source, destination])
        
        if result.returncode == 0:
            print(f"  \033[32m✓ Merge completed\033[0m")
            return True
        else:
            print(f"  \033[33m⚠ Merge cancelled or failed\033[0m")
            return False
    except FileNotFoundError:
        print(f"  \033[31m✗ vimdiff not found. Please install vim or use overwrite option.\033[0m")
        return False
    except Exception as e:
        print(f"  \033[31m✗ Error during merge: {e}\033[0m")
        return False
