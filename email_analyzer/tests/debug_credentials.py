from loguru import logger
import json
from pathlib import Path

def debug_json_files():
    """Debug function to check JSON contents"""
    creds_dir = Path("config/credentials")
    
    # Map of our JSON files
    files = {
        'mark0025.json': 'Gmail Account',
        'marklhb.json': 'LHB Account',
        'marktheairei.json': 'AIREI Account'
    }
    
    for file_name, description in files.items():
        try:
            logger.info(f"\nChecking {description} ({file_name})...")
            with open(creds_dir / file_name) as f:
                data = json.load(f)
                # Log structure without exposing actual credentials
                logger.info(f"Keys in file: {list(data.keys())}")
                
                # Check if we have what we need
                has_email = any('email' in k.lower() for k in data.keys())
                has_password = any('password' in k.lower() for k in data.keys())
                
                logger.info(f"Has email field: {has_email}")
                logger.info(f"Has password field: {has_password}")
                
                # Show exact key names (without values)
                for key in data.keys():
                    logger.info(f"Found key: {key}")
                    
        except Exception as e:
            logger.error(f"Error reading {file_name}: {str(e)}")

if __name__ == "__main__":
    debug_json_files() 