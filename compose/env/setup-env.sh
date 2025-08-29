#!/bin/bash

# DVSwitch Environment Setup Script
# Copies example environment files to concrete .env files

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory to ensure relative paths work
cd "$SCRIPT_DIR"

echo "DVSwitch Environment Setup"
echo "=========================="
echo ""

# Define the file mappings as parallel arrays
EXAMPLE_FILES=(
    "common.env.example"
    "mmdvm_bridge.env.example"
    "analog_bridge.env.example"
    "analog_reflector.env.example"
)

CONCRETE_FILES=(
    ".env.common"
    ".env.mmdvm_bridge"
    ".env.analog_bridge"
    ".env.analog_reflector"
)

# Check for existing files
existing_files=()
for i in "${!EXAMPLE_FILES[@]}"; do
    example_file="${EXAMPLE_FILES[$i]}"
    concrete_file="${CONCRETE_FILES[$i]}"
    if [[ -f "$concrete_file" ]]; then
        existing_files+=("$concrete_file")
    fi
done

# If any files exist, ask for confirmation
if [[ ${#existing_files[@]} -gt 0 ]]; then
    echo "The following environment files already exist:"
    for file in "${existing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    read -p "Do you want to overwrite these files? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. No files were modified."
        exit 0
    fi
fi

# Copy the files
echo "Copying environment files..."
for i in "${!EXAMPLE_FILES[@]}"; do
    example_file="${EXAMPLE_FILES[$i]}"
    concrete_file="${CONCRETE_FILES[$i]}"
    
    if [[ -f "$example_file" ]]; then
        cp "$example_file" "$concrete_file"
        echo "  ✓ Copied $example_file -> $concrete_file"
    else
        echo "  ✗ Warning: $example_file not found"
    fi
done

echo ""
echo "Setup complete! Next steps:"
echo "1. Edit .env.common with your actual values:"
echo "   - MY_CALLSIGN=YOUR_CALLSIGN"
echo "   - MY_DMR_ID=YOUR_DMR_ID"
echo "   - BM_MASTER_HOST=YOUR_BM_MASTER"
echo "   - BM_PASSWORD=YOUR_BM_PASSWORD"
echo ""
echo "2. Edit service-specific files if needed:"
echo "   - .env.mmdvm_bridge"
echo "   - .env.analog_bridge"
echo "   - .env.analog_reflector"
echo ""
echo "3. Test your configuration:"
echo "   docker compose -f compose/docker-compose.local.yaml --profile local up --build"
