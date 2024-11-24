#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Log function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] SUCCESS:${NC} $1"
}

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    log "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements using uv
log "Installing requirements with uv..."
uv pip install -r requirements.txt

# Run the generator
log "Generating API dashboard..."
python generate_api_dashboard_data.py

# Start the server on port 8122
log "Starting server on port 8122..."
python -m http.server 8122 