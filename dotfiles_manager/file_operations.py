#!/usr/bin/env python3
"""File operations for dotfiles manager."""

import os
import shutil

def copy_file(source, destination):
    """Copy or overwrite a file from source to destination."""
    source = os.path.expandvars(source)
    destination = os.path.expandvars(destination)
    
    try:
        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(destination)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
        
        # Copy the file
        shutil.copy2(source, destination)
        print(f"  \033[32m✓ Copied {source} to {destination}\033[0m")
        return True
    except Exception as e:
        print(f"  \033[31m✗ Error copying file: {e}\033[0m")
        return False

def sync_directory(source, destination):
    """Sync directory by copying only missing files and subdirectories."""
    source = os.path.expandvars(source)
    destination = os.path.expandvars(destination)
    
    if not os.path.exists(source):
        print(f"  \033[31m✗ Source directory does not exist: {source}\033[0m")
        return False
    
    try:
        # Create destination directory if it doesn't exist
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)
        
        copied_count = 0
        
        # Walk through source directory
        for root, dirs, files in os.walk(source):
            # Calculate relative path from source
            rel_dir = os.path.relpath(root, source)
            if rel_dir == '.':
                dest_dir = destination
            else:
                dest_dir = os.path.join(destination, rel_dir)
            
            # Create subdirectories if they don't exist
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)
                print(f"    \033[36m+ Created directory: {rel_dir}\033[0m")
            
            # Copy files that don't exist in destination
            for file in files:
                source_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                
                if not os.path.exists(dest_file):
                    shutil.copy2(source_file, dest_file)
                    rel_file = os.path.join(rel_dir, file) if rel_dir != '.' else file
                    print(f"    \033[32m+ Copied: {rel_file}\033[0m")
                    copied_count += 1
        
        if copied_count > 0:
            print(f"  \033[32m✓ Synced directory: {copied_count} files copied\033[0m")
        else:
            print(f"  \033[32m✓ Directory already in sync\033[0m")
        return True
        
    except Exception as e:
        print(f"  \033[31m✗ Error syncing directory: {e}\033[0m")
        return False

def get_missing_files_in_directory(source, destination):
    """Get list of files that exist in source but not in destination."""
    source = os.path.expandvars(source)
    destination = os.path.expandvars(destination)
    
    missing_files = []
    
    if not os.path.exists(source):
        return missing_files
    
    if not os.path.exists(destination):
        # If destination doesn't exist, all files are missing
        for root, dirs, files in os.walk(source):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), source)
                missing_files.append(rel_path)
        return missing_files
    
    # Compare files in both directories
    for root, dirs, files in os.walk(source):
        for file in files:
            source_file = os.path.join(root, file)
            rel_path = os.path.relpath(source_file, source)
            dest_file = os.path.join(destination, rel_path)
            
            if not os.path.exists(dest_file):
                missing_files.append(rel_path)
    
    return missing_files

def get_directory_file_pairs(source, destination):
    """Get pairs of (source_file, dest_file) for all files in source directory."""
    source = os.path.expandvars(source)
    destination = os.path.expandvars(destination)
    
    file_pairs = []
    
    if not os.path.exists(source):
        return file_pairs
    
    for root, dirs, files in os.walk(source):
        for file in files:
            source_file = os.path.join(root, file)
            rel_path = os.path.relpath(source_file, source)
            dest_file = os.path.join(destination, rel_path)
            file_pairs.append((source_file, dest_file, rel_path))
    
    return file_pairs
