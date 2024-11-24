import os
from pathlib import Path
from dotenv import load_dotenv

# Load main .env file
load_dotenv()

# Load LastPass credentials from @workstation
WORKSTATION_PATH = Path.home() / "@workstation"
LASTPASS_CREDS_PATH = WORKSTATION_PATH / '.env-lastpass-creds'

if LASTPASS_CREDS_PATH.exists():
    load_dotenv(LASTPASS_CREDS_PATH)
else:
    raise FileNotFoundError("LastPass credentials not found in @workstation folder")

# Database Configuration
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", 5432),
    "database": os.getenv("POSTGRES_DB", "email_analytics"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "")
}

# Email Configuration
EMAIL_ACCOUNTS = {
    "primary": {
        "username": os.getenv("HTTPS___ACCOUNTS_GOOGLE_COM_SIGNIN_V2_IDENTIFIER_USERNAME"),
        "password": os.getenv("HTTPS___ACCOUNTS_GOOGLE_COM_SIGNIN_V2_IDENTIFIER_PASSWORD"),
        "imap_server": "imap.gmail.com"
    }
} 