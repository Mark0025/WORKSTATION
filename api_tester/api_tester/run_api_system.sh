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

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    log "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements using uv
log "Installing requirements..."
uv pip install pandas pendulum loguru aiohttp python-dotenv graphviz

# Run name validation
log "Validating API names..."
python tools/validate_names.py

# Generate dashboard
log "Generating dashboard..."
python generate_api_dashboard_data.py

# Start the server
log "Starting visualization server..."
python -m http.server 8122
