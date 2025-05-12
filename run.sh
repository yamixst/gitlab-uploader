#!/bin/bash

# Exit on error
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"

# Function to print colored text
print_color() {
    COLOR=$1
    TEXT=$2
    echo -e "\033[${COLOR}m${TEXT}\033[0m"
}

print_step() {
    print_color "36" "\n==> $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_color "31" "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    print_step "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    print_color "32" "Virtual environment created successfully"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source "${VENV_DIR}/bin/activate"
print_color "32" "Virtual environment activated"

# Install dependencies
print_step "Installing required packages..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
print_color "32" "Requirements installed successfully"

# Run the application
print_step "Starting GitLab Uploader..."
python gitlab_uploader.py

# Deactivate virtual environment (this line will only be reached if the application is closed)
deactivate

print_color "32" "Session completed"