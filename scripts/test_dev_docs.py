import requests
from pathlib import Path
from loguru import logger
import sys
import traceback

def test_dev_docs():
    """Test dev docs server components"""
    try:
        # 1. Check directories
        docs_dir = Path("DEV-MAN")
        if not docs_dir.exists():
            logger.error("DEV-MAN directory missing")
            return False
            
        # 2. Check documentation files
        md_files = list(docs_dir.glob("**/*.md"))
        if not md_files:
            logger.error("No markdown files found")
            return False
        logger.info(f"Found {len(md_files)} markdown files")
        
        # 3. Try to start server
        try:
            logger.debug("Attempting to import dev_docs_server...")
            from crews.visualization.dev_docs_server import app
            logger.info("Server module imported successfully")
        except Exception as e:
            logger.error(f"Failed to import server: {str(e)}")
            logger.debug("Full traceback:")
            logger.debug(traceback.format_exc())
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        logger.debug(traceback.format_exc())
        return False

if __name__ == "__main__":
    if not test_dev_docs():
        sys.exit(1) 