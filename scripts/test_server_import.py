from loguru import logger
import sys
import traceback

def test_import():
    """Test importing the server module directly"""
    try:
        logger.info("Testing server import...")
        
        # Try importing with full path
        import crews.visualization.dev_docs_server
        logger.info("✅ Basic import successful")
        
        # Try creating app
        app = crews.visualization.dev_docs_server.app
        logger.info("✅ App creation successful")
        
        # Try getting documentation
        docs = crews.visualization.dev_docs_server.get_documentation_tree()
        logger.info(f"✅ Found {len(docs)} documentation files")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Import test failed: {str(e)}")
        logger.debug("Full traceback:")
        logger.debug(traceback.format_exc())
        return False

if __name__ == "__main__":
    if not test_import():
        sys.exit(1) 