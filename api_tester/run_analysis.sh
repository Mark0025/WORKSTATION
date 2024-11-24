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

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    log "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements using uv
log "Installing requirements..."
uv pip install pandas crewai crewai-tools aiohttp loguru python-dotenv

# Run analysis
log "Running API analysis..."
python -m pytest tests/test_analyzer.py -v --log-cli-level=INFO

# Check results
if [ -f ".env.working" ] && [ -f ".env.not-working" ]; then
    success "Analysis completed successfully"
    success "Check:"
    success "  - .env.working for working APIs"
    success "  - .env.not-working for non-working APIs"
    success "  - logs/api_analysis_report.md for detailed analysis"
else
    error "Analysis failed to generate environment files"
fi 