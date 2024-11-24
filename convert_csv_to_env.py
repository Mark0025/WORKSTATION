import csv
import json
import glob
import os
import logging
import shutil
from typing import Dict, Any
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_workstation_folder() -> Path:
    """Create @workstation folder if it doesn't exist and return path."""
    workstation_path = Path.home() / "@workstation"
    workstation_path.mkdir(exist_ok=True)
    return workstation_path

def csv_to_json() -> None:
    """Convert CSV files to JSON and create environment credentials file."""
    try:
        # Get @workstation folder path
        workstation_path = create_workstation_folder()
        
        # Dictionary to store all credentials
        all_creds: Dict[str, Any] = {}
        
        # Find all CSV files in current directory
        csv_files = glob.glob("*.csv")
        if not csv_files:
            logging.warning("No CSV files found in current directory")
            return
        
        logging.info(f"Found {len(csv_files)} CSV files to process")
        
        for csv_file in csv_files:
            try:
                with open(csv_file, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)
                    # Convert each row to dictionary entries
                    for row in csv_reader:
                        # Use URL or name as key
                        key = row.get('url', row.get('name', f'entry_{len(all_creds)}'))
                        all_creds[key] = {
                            'username': row.get('username', ''),
                            'password': row.get('password', '')
                        }
                logging.info(f"Processed {csv_file} successfully")
            except Exception as e:
                logging.error(f"Error processing {csv_file}: {str(e)}")
                continue
        
        if not all_creds:
            logging.warning("No credentials were extracted from CSV files")
            return
            
        # Save credentials.json to @workstation folder
        creds_path = workstation_path / 'credentials.json'
        with open(creds_path, 'w') as json_file:
            json.dump(all_creds, json_file, indent=2)
        logging.info(f"Created credentials.json in {workstation_path}")
        
        # Create .env-lastpass-creds in @workstation folder
        lastpass_env_path = workstation_path / '.env-lastpass-creds'
        with open(lastpass_env_path, 'w') as env_file:
            for key, value in all_creds.items():
                # Convert special characters in key to underscore
                safe_key = ''.join(c if c.isalnum() else '_' for c in key)
                env_file.write(f"{safe_key.upper()}_USERNAME={value['username']}\n")
                env_file.write(f"{safe_key.upper()}_PASSWORD={value['password']}\n")
        logging.info(f"Created .env-lastpass-creds in {workstation_path}")
        
        # Create a template .env file in project directory
        with open('.env', 'w') as env_file:
            env_file.write(f"LASTPASS_CREDS_PATH={lastpass_env_path}\n")
            env_file.write("# Add your project-specific environment variables below\n")
        logging.info("Created .env template file")
        
        # Create .gitignore if it doesn't exist
        if not os.path.exists('.gitignore'):
            with open('.gitignore', 'w') as gitignore:
                gitignore.write("# Sensitive files\n")
                gitignore.write(".env\n")
                gitignore.write("*.csv\n")
                gitignore.write("@workstation/\n")
        logging.info("Updated .gitignore")
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

def load_lastpass_creds():
    """Helper function to load LastPass credentials in other scripts."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        creds_path = os.getenv('LASTPASS_CREDS_PATH')
        if not creds_path or not os.path.exists(creds_path):
            raise FileNotFoundError("LastPass credentials file not found")
            
        load_dotenv(creds_path)
        return True
    except Exception as e:
        logging.error(f"Error loading LastPass credentials: {str(e)}")
        return False

if __name__ == "__main__":
    csv_to_json() 