#!/usr/bin/env python3
"""Main entry point for the modular dotfiles manager."""

import sys
from .checker import check_all_diffs
from .listing import list_dotfiles
from .add_dotfile import add_dotfile

def main():
    """Main function."""
    if len(sys.argv) == 1:
        check_all_diffs()
    elif sys.argv[1] == "diff":
        check_all_diffs()
    elif sys.argv[1] == "list":
        list_dotfiles()
    elif sys.argv[1] == "add" and len(sys.argv) >= 5:
        if len(sys.argv) == 5:
            # Auto-detect type
            add_dotfile(sys.argv[2], sys.argv[3], sys.argv[4])
        elif len(sys.argv) == 6:
            # Explicit type specified
            add_dotfile(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        else:
            print("Too many arguments for add command")
    else:
        print("Usage:")
        print("  python -m dotfiles_manager [diff]         - Check diffs (default)")
        print("  python -m dotfiles_manager list           - List dotfiles")
        print("  python -m dotfiles_manager add <name> <source> <dest> [type]")
        print("    type: 'file' or 'directory' (auto-detected if not specified)")

if __name__ == "__main__":
    main()
