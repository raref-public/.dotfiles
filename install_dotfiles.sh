#!/usr/bin/bash

# run this script to configure dotfiles!
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -h, --help      Show this help message and exit"
    echo "  -l, --lean      Run in lean mode"
    echo "  -b, --bulk      Run in bulk mode"
    echo "  -s, --sec       Run in sec mode"
}

LEAN_MODE=false
BULK_MODE=false
SEC_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -l|--lean)
            LEAN_MODE=true
            shift
            ;;
        -b|--bulk)
            BULK_MODE=true
            shift
            ;;
        -s|--sec)
            SEC_MODE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if [ "$LEAN_MODE" = true ]; then
    echo "Running in lean mode..."
    # Add lean mode code here
fi

if [ "$BULK_MODE" = true ]; then
    echo "Running in bulk mode..."
    # Add bulk mode code here
fi

if [ "$SEC_MODE" = true ]; then
    echo "Running in sec mode..."
    # Add sec mode code here
fi