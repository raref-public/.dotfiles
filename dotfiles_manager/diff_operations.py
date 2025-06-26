#!/usr/bin/env python3
"""Diff operations for dotfiles manager."""

import os
import subprocess

def diff_files(source, destination):
    """Compare two files using diff command."""
    source = os.path.expandvars(source)
    destination = os.path.expandvars(destination)
    
    if not os.path.exists(source):
        return f"Source missing: {source}"
    
    if not os.path.exists(destination):
        return f"Destination missing: {destination}"
    
    try:
        result = subprocess.run(["diff", source, destination], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return "Files identical"
        else:
            return result.stdout
    except Exception as e:
        return f"Diff error: {e}"
