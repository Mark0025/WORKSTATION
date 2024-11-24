#!/bin/bash

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies using uv
uv pip install -r requirements.txt 