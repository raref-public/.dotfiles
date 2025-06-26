#!/usr/bin/env python3
"""Main checking functionality for dotfiles manager."""

import os
from .config import load_or_create_config
from .diff_operations import diff_files
from .file_operations import copy_file, sync_directory, get_missing_files_in_directory, get_directory_file_pairs
from .merge_operations import merge_files

def check_all_diffs():
    """Check diffs for all configured dotfiles."""
    config = load_or_create_config()
    
    for name, paths in config.get("dotfiles", {}).items():
        print(f"\n{name}:")
        source = paths.get("source", "")
        dest = paths.get("destination", "")
        file_type = paths.get("type", "file")  # Default to file if type not specified
        
        if not source or not dest:
            print("  Missing source or destination")
            continue
        
        if file_type == "directory":
            check_directory_diff(source, dest)
        else:
            check_file_diff(source, dest)

def check_file_diff(source, dest):
    """Check diff for a single file."""
    diff_output = diff_files(source, dest)
    
    if diff_output == "Files identical":
        print("  \033[32m✓ Identical\033[0m")
    elif "missing" in diff_output.lower():
        print(f"  \033[31m✗ {diff_output}\033[0m")
        
        # Check if source exists and destination is missing
        source_expanded = os.path.expandvars(source)
        dest_expanded = os.path.expandvars(dest)
        
        if os.path.exists(source_expanded) and not os.path.exists(dest_expanded):
            response = input(f"  Copy {source} to {dest}? (y/n): ").lower().strip()
            match response:
                case 'y' | 'yes':
                    copy_file(source, dest)
                case _:
                    print("  \033[33m⚠ Skipped\033[0m")
    else:
        print("  \033[31m✗ Files differ\033[0m")
        # Show first few lines of diff
        lines = diff_output.split('\n')[:5]
        for line in lines:
            if line.strip():
                print(f"    {line}")
        
        # Ask user what to do about the differences
        print("  What would you like to do?")
        print("    [o] Overwrite destination with source")
        print("    [m] Merge files interactively")
        print("    [s] Skip this file")
        
        response = input("  Choose (o/m/s): ").lower().strip()
        
        match response:
            case 'o' | 'overwrite':
                copy_file(source, dest)
            case 'm' | 'merge':
                merge_files(source, dest)
            case _:
                print("  \033[33m⚠ Skipped\033[0m")

def check_directory_diff(source, dest):
    """Check diff for a directory."""
    source_expanded = os.path.expandvars(source)
    dest_expanded = os.path.expandvars(dest)
    
    if not os.path.exists(source_expanded):
        print(f"  \033[31m✗ Source directory missing: {source}\033[0m")
        return
    
    if not os.path.exists(dest_expanded):
        print(f"  \033[31m✗ Destination directory missing: {dest}\033[0m")
        response = input(f"  Create and sync directory {dest}? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            sync_directory(source, dest)
        else:
            print("  \033[33m⚠ Skipped\033[0m")
        return
    
    # Check for missing files
    missing_files = get_missing_files_in_directory(source, dest)
    if missing_files:
        print(f"  \033[33m⚠ Missing {len(missing_files)} files in destination:\033[0m")
        for missing_file in missing_files[:5]:  # Show first 5 missing files
            print(f"    - {missing_file}")
        if len(missing_files) > 5:
            print(f"    ... and {len(missing_files) - 5} more")
        
        response = input(f"  Copy missing files to {dest}? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            sync_directory(source, dest)
        else:
            print("  \033[33m⚠ Skipped copying missing files\033[0m")
    
    # Check for differences in existing files
    file_pairs = get_directory_file_pairs(source, dest)
    different_files = []
    
    for source_file, dest_file, rel_path in file_pairs:
        if os.path.exists(dest_file):
            diff_output = diff_files(source_file, dest_file)
            if diff_output != "Files identical" and "missing" not in diff_output.lower():
                different_files.append((source_file, dest_file, rel_path))
    
    if different_files:
        print(f"  \033[31m✗ {len(different_files)} files differ:\033[0m")
        for source_file, dest_file, rel_path in different_files[:3]:  # Show first 3 different files
            print(f"    - {rel_path}")
        if len(different_files) > 3:
            print(f"    ... and {len(different_files) - 3} more")
        
        print("  What would you like to do?")
        print("    [o] Overwrite all different files with source versions")
        print("    [i] Handle each file individually")
        print("    [s] Skip all different files")
        
        response = input("  Choose (o/i/s): ").lower().strip()
        
        match response:
            case 'o' | 'overwrite':
                for source_file, dest_file, rel_path in different_files:
                    copy_file(source_file, dest_file)
            case 'i' | 'individual':
                for source_file, dest_file, rel_path in different_files:
                    print(f"\n  File: {rel_path}")
                    diff_output = diff_files(source_file, dest_file)
                    lines = diff_output.split('\n')[:3]
                    for line in lines:
                        if line.strip():
                            print(f"    {line}")
                    
                    print("    [o] Overwrite with source")
                    print("    [m] Merge interactively")
                    print("    [s] Skip this file")
                    
                    file_response = input("    Choose (o/m/s): ").lower().strip()
                    match file_response:
                        case 'o' | 'overwrite':
                            copy_file(source_file, dest_file)
                        case 'm' | 'merge':
                            merge_files(source_file, dest_file)
                        case _:
                            print(f"    \033[33m⚠ Skipped {rel_path}\033[0m")
            case _:
                print("  \033[33m⚠ Skipped all different files\033[0m")
    
    if not missing_files and not different_files:
        print("  \033[32m✓ Directory in sync\033[0m")
