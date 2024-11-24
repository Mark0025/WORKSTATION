import requests
from loguru import logger
import time
import sys

def verify_server():
    """Verify the dev docs server is running and responding"""
    MAX_RETRIES = 5
    RETRY_DELAY = 2
    
    logger.info("Verifying dev docs server...")
    
    for i in range(MAX_RETRIES):
        try:
            # Check /dev endpoint instead of root
            response = requests.get("http://localhost:8010/dev")
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response content: {response.text[:200]}")  # First 200 chars
            
            if response.status_code != 200:
                raise Exception(f"Server returned {response.status_code}")
                
            # Check health endpoint
            health = requests.get("http://localhost:8010/dev/health").json()
            logger.debug(f"Health check response: {health}")
            
            if health["status"] != "healthy":
                raise Exception(f"Unhealthy server: {health}")
                
            logger.success("Server verification passed!")
            return True
            
        except requests.ConnectionError:
            if i < MAX_RETRIES - 1:
                logger.warning(f"Server not responding, retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Server failed to respond after multiple retries")
                return False
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return False
            
    return False

if __name__ == "__main__":
    if not verify_server():
        sys.exit(1) 