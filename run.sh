#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to check if PostgreSQL is running
check_postgres() {
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker ps | grep -q postgres; then
        log "Starting PostgreSQL container..."
        docker run --name email-analyzer-postgres \
            -e POSTGRES_USER=user \
            -e POSTGRES_PASSWORD=password \
            -e POSTGRES_DB=emaildb \
            -p 5432:5432 \
            -d postgres:13
        
        # Wait for PostgreSQL to be ready
        sleep 5
    fi
}

# Function to check if port is in use
check_port() {
    nc -z localhost $1 >/dev/null 2>&1
    return $?
}

# Function to find next available port
find_available_port() {
    local port=$1
    while check_port $port; do
        log "Port $port is in use, trying next port..."
        port=$((port + 1))
    done
    echo $port
}

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    error "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create and activate virtual environment
log "Creating virtual environment..."
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies using uv
log "Installing dependencies with uv..."
uv pip install -r requirements.txt

# Ensure PostgreSQL is running
check_postgres

# Initialize alembic if not already initialized
if [ ! -f "alembic.ini" ]; then
    log "Initializing Alembic..."
    alembic init alembic
    
    # Update alembic.ini with database URL
    sed -i.bak "s|sqlalchemy.url = .*|sqlalchemy.url = postgresql://user:password@localhost:5432/emaildb|" alembic.ini
fi

# Run database migrations
log "Running database migrations..."
alembic upgrade head || {
    error "Database migration failed"
    exit 1
}

# Find available port (store in variable)
PORT=$(find_available_port 8000)
log "Using port $PORT"

# Start the application with the found port
log "Starting application..."
uvicorn backend.app.main:app --reload --log-level debug --port "$PORT"