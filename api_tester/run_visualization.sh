#!/bin/bash

# Activate virtual environment if it exists, create if it doesn't
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi
source .venv/bin/activate

# Install all dependencies at once
uv pip install -r requirements.txt

# Run visualization
python generate_visualization.py

# Start server
python -m http.server 8122
