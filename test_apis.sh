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

# Ensure virtual environment is activated
source .venv/bin/activate

# Install required packages
log "Installing required packages..."
uv pip install aiohttp pytest-asyncio

# Run API tests
log "Running API tests..."
pytest backend/app/tests/test_apis.py -v --log-cli-level=INFO

# Check if .env.test was created
if [ -f ".env.test" ]; then
    success "API tests completed. Check .env.test for working APIs"
    success "Detailed report available in logs/api_test_report.md"
else
    error "API tests failed to generate .env.test"
fi 