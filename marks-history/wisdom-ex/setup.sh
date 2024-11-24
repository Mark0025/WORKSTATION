#!/bin/bash

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies using uv
uv pip install -r requirements.txt 