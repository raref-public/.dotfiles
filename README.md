# Linux Configuration Files

This repository contains various configuration files for Linux systems, tailored for optimal performance and usability. It includes a powerful dotfiles manager application that helps you synchronize and manage your configuration files and directories.

## Repository Structure

- `.files/` - Individual configuration files (e.g., .vimrc, .tmux.conf, .bash_profile)
- `.bashfuncs/` - Bash function definitions and utilities
- `.secfuncs/` - Security-related functions
- `.zshfuncs/` - Zsh function definitions
- `cloud-init/` - Cloud initialization configurations
- `dotfiles_manager/` - Python application for managing dotfiles
- `dotfiles.json` - Configuration file defining dotfile mappings
- `install_dotfiles.sh` - Legacy installation script

## Dotfiles Manager

The `dotfiles_manager` is a Python application that provides intelligent synchronization and management of both individual files and entire directories. It supports diff operations, missing file detection, and interactive management.

### Features

- **File and Directory Support**: Handle both individual files and entire directory structures
- **Type Detection**: Automatically detects whether a source is a file or directory
- **Smart Synchronization**: Only copies missing files, preserves existing ones
- **Diff Operations**: Compare files and directories with detailed reporting
- **Interactive Management**: Prompts for user decisions on conflicts and missing files
- **Recursive Directory Handling**: Copies all subdirectories and files recursively
- **Missing File Detection**: Identifies files present in source but missing in destination

### Installation

No installation required. The dotfiles manager runs directly from the repository:

```bash
cd /path/to/.dotfiles
python3 -m dotfiles_manager
```

### Configuration

The `dotfiles.json` file defines your dotfile mappings. Each entry includes:

- `type`: Either "file" or "directory"
- `source`: Path to the source file or directory (relative to repository root)
- `destination`: Target path (supports environment variables like $HOME)

Example configuration:
```json
{
  "dotfiles": {
    "_vimrc": {
      "type": "file",
      "source": "./.files/.vimrc",
      "destination": "$HOME/.vimrc"
    },
    ".tmux.conf": {
      "type": "file",
      "source": "./.files/.tmux.conf",
      "destination": "$HOME/.tmux.conf"
    },
    ".bashfuncs": {
      "type": "directory",
      "source": "./.bashfuncs",
      "destination": "$HOME/.bashfuncs"
    }
  }
}
```

### Usage

#### List Configured Dotfiles
```bash
python3 -m dotfiles_manager list
```
Shows all configured dotfiles with type indicators:
- 📄 for files
- 📁 for directories

#### Check Differences (Default Command)
```bash
python3 -m dotfiles_manager
# or explicitly:
python3 -m dotfiles_manager diff
```

For **files**, this will:
- Compare source and destination files
- Show diff output for different files
- Prompt to copy missing files
- Offer merge options for conflicts

For **directories**, this will:
- Check for missing files in destination
- Compare existing files individually
- Report directory synchronization status
- Offer batch or individual file handling

#### Add New Dotfiles
```bash
# Auto-detect type (recommended)
python3 -m dotfiles_manager add "config_name" "./source/path" "$HOME/destination"

# Specify type explicitly
python3 -m dotfiles_manager add "config_name" "./source/path" "$HOME/destination" file
python3 -m dotfiles_manager add "config_name" "./source/path" "$HOME/destination" directory
```

### File Operations

#### For Files (`type: "file"`)
- Uses standard `diff` command for comparison
- Copies individual files with `shutil.copy2`
- Preserves file metadata (timestamps, permissions)
- Offers interactive merge options

#### For Directories (`type: "directory"`)
- **Smart Sync**: Only copies files that don't exist in destination
- **Recursive**: Handles nested directory structures
- **Preserves Structure**: Creates necessary subdirectories
- **Individual File Diffs**: Compares existing files one by one
- **Batch Operations**: Option to handle all different files at once

### Interactive Options

When differences are detected, the manager offers several options:

#### For Files:
- **[o] Overwrite**: Replace destination with source
- **[m] Merge**: Interactive merge using external tools
- **[s] Skip**: Leave file unchanged

#### For Directories:
- **Missing Files**: Option to copy all missing files
- **Different Files**: 
  - **[o] Overwrite all**: Replace all different files
  - **[i] Individual**: Handle each file separately
  - **[s] Skip all**: Leave all files unchanged

### Examples

#### Basic Usage
```bash
# Check all dotfiles status
python3 -m dotfiles_manager

# List configured dotfiles
python3 -m dotfiles_manager list

# Add a new configuration file
python3 -m dotfiles_manager add "gitconfig" "./.files/.gitconfig" "$HOME/.gitconfig"

# Add a configuration directory
python3 -m dotfiles_manager add "nvim" "./nvim" "$HOME/.config/nvim"
```

#### Sample Output
```
Configured dotfiles:
  📄 _vimrc (file): ./.files/.vimrc -> $HOME/.vimrc
  📄 .tmux.conf (file): ./.files/.tmux.conf -> $HOME/.tmux.conf
  📁 .bashfuncs (directory): ./.bashfuncs -> $HOME/.bashfuncs

_vimrc:
  ✓ Identical

.tmux.conf:
  ✗ Destination missing: /home/user/.tmux.conf
  Copy ./.files/.tmux.conf to $HOME/.tmux.conf? (y/n): 

.bashfuncs:
  ⚠ Missing 3 files in destination:
    - function1.sh
    - function2.sh
    - utils/helper.sh
  Copy missing files to $HOME/.bashfuncs? (y/n):
```

### Advanced Features

#### Directory Synchronization
- Creates missing subdirectories automatically
- Preserves existing files (no overwrite unless requested)
- Detailed reporting of copied files and created directories
- Handles complex nested structures

#### Conflict Resolution
- Shows diff previews for conflicting files
- Individual file handling within directories
- Merge support for text files
- Batch operations for multiple conflicts

#### Type Auto-Detection
When adding new dotfiles without specifying type:
- Checks if source path exists
- Uses `os.path.isdir()` to determine if it's a directory
- Defaults to "file" if source doesn't exist

### Error Handling

The manager includes robust error handling:
- Missing source files/directories
- Permission issues
- Invalid paths
- Malformed configuration files
- Network/filesystem errors

### Compatibility

- **Python**: Requires Python 3.6+ (uses match/case statements)
- **Operating System**: Linux/Unix systems
- **Dependencies**: Uses only Python standard library
- **Shell**: Works with bash, zsh, and other POSIX shells

## Legacy Installation

The repository also includes `install_dotfiles.sh` for traditional shell-based installation, but the Python dotfiles manager is recommended for its advanced features and better error handling.

## Contributing

Feel free to explore and customize these configuration files to fit your needs. The dotfiles manager is designed to be extensible and can be modified to support additional features as needed.
