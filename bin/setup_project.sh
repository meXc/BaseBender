#!/bin/bash

# Check for Python version
PYTHON_MIN_VERSION="3.12"
PYTHON_CURRENT_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

if printf '%s\n' "$PYTHON_MIN_VERSION" "$PYTHON_CURRENT_VERSION" | sort -V -C; then
    echo "Python version check passed: $PYTHON_CURRENT_VERSION (>= $PYTHON_MIN_VERSION)"
else
    echo "Error: Python version $PYTHON_CURRENT_VERSION is older than required $PYTHON_MIN_VERSION."
    echo "Please update your Python installation."
    exit 1
fi

# Check for Poetry installation
if ! command -v poetry &> /dev/null
then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Poetry. Please install it manually."
        exit 1
    fi
    echo "Poetry installed successfully."
else
    echo "Poetry is already installed."
fi

# Install project dependencies
echo "Installing project dependencies with Poetry..."
poetry install
if [ $? -ne 0 ]; then
    echo "Error: Failed to install project dependencies."
    exit 1
fi
echo "Project dependencies installed successfully."

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
poetry run pre-commit install
if [ $? -ne 0 ]; then
    echo "Error: Failed to install pre-commit hooks."
    exit 1
fi
echo "Pre-commit hooks installed successfully."

# Run project-specific update script
echo "Running bin/update script..."
./bin/update
if [ $? -ne 0 ]; then
    echo "Error: bin/update script failed."
    exit 1
fi
echo "bin/update script executed successfully."

echo "Project setup complete!"
