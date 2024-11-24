from pathlib import Path
import subprocess
from loguru import logger
import sys

def install_packages():
    """Install both workstation and timeline packages"""
    try:
        # Install workstation package
        logger.info("Installing workstation package...")
        subprocess.run(["uv", "pip", "install", "-e", "."], check=True)
        
        # Install timeline package
        logger.info("Installing timeline package...")
        os.chdir("timeline")
        subprocess.run(["uv", "pip", "install", "-e", "."], check=True)
        
        logger.success("Both packages installed successfully!")
        
    except Exception as e:
        logger.error(f"Installation failed: {str(e)}")
        sys.exit(1)

def verify_installation():
    """Verify both packages are installed correctly"""
    try:
        # Test workstation import
        import workstation
        logger.info("✅ Workstation package verified")
        
        # Test timeline import
        import timeline
        logger.info("✅ Timeline package verified")
        
        return True
    except ImportError as e:
        logger.error(f"Package verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    install_packages()
    verify_installation() 