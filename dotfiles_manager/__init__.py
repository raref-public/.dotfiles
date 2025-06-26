#!/usr/bin/env python3
"""Modular dotfiles manager package."""

from .config import load_or_create_config, save_config
from .file_operations import copy_file
from .merge_operations import merge_files
from .diff_operations import diff_files
from .checker import check_all_diffs
from .listing import list_dotfiles
from .add_dotfile import add_dotfile
from .main import main

__all__ = [
    'load_or_create_config',
    'save_config',
    'copy_file',
    'merge_files',
    'diff_files',
    'check_all_diffs',
    'list_dotfiles',
    'add_dotfile',
    'main'
]
