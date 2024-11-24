from pathlib import Path
import subprocess
import sys
import os

# First install loguru
subprocess.run(["uv", "pip", "install", "loguru==0.6.0"], check=True)

# Now we can import loguru
from loguru import logger

def install_project():
    """Install project with proper dependencies"""
    try:
        # Add timeline to Python path
        timeline_path = Path(__file__).parent.parent
        sys.path.append(str(timeline_path))
        
        # Install core dependencies first
        logger.info("Installing core dependencies...")
        subprocess.run([
            "uv", "pip", "install",
            "sqlalchemy>=2.0.23",
            "watchdog>=3.0.0",
            "rich>=13.7.0",
            "click>=8.1.7",
        ], check=True)
        
        # Install AI dependencies
        logger.info("Installing AI dependencies...")
        subprocess.run([
            "uv", "pip", "install",
            "crewai>=0.80.0",
            "langchain>=0.3.8",
            "langchain-openai>=0.2.9",
            "openai>=1.0.0",
        ], check=True)
        
        # Then install the project
        logger.info("Installing project in editable mode...")
        subprocess.run(["uv", "pip", "install", "-e", "."], check=True)
        
        # Initialize database
        logger.info("Initializing database...")
        from timeline.init_db import init_database
        init_database()
        
        logger.success("Installation complete!")
        
    except Exception as e:
        logger.error(f"Installation failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    install_project() 