#!/bin/bash

# This is a wrapper script to run the Python application.

# Set the Python interpreter
PYTHON_EXECUTABLE="python3"

# Check if the Python script exists
if [ ! -f "src/main.py" ]; then
    echo "Error: src/main.py not found. Make sure you are in the project root directory."
    exit 1
fi

# Execute the Python script with all command-line arguments
# The "$@" passes all arguments from the shell script to the Python script
$PYTHON_EXECUTABLE src/main.py "$@"
