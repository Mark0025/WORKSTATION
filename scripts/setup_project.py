from pathlib import Path
import subprocess
import sys
from loguru import logger
from diagram_watcher import watch_diagrams
import threading

def setup_project():
    """Setup project structure and dependencies"""
    try:
        # Create necessary directories
        dirs = [
            "crews",
            "timeline",
            "timeline/data",
            "DEV-MAN/diagrams",
            "DEV-MAN/docs",
        ]
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {d}")

        # Install dependencies
        subprocess.run(["uv", "pip", "install", "-e", "."], check=True)
        
        # Initialize database
        from timeline.init_db import init_database
        init_database()
        
        logger.success("Project setup complete!")
        
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_project() 