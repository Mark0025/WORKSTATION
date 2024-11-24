import json
import os
from typing import Dict
from pathlib import Path
from dotenv import load_dotenv

class CredentialsManager:
    def __init__(self):
        load_dotenv()
        self.credentials_path = Path("config/credentials")
        self.email_accounts = {}
        self.load_all_credentials()

    def load_all_credentials(self):
        # Load LastPass credentials
        lastpass_creds = self._load_json_file("lastpass_credentials.json")
        
        # Load Google API credentials
        self.google_creds = {
            "mark0025": self._load_json_file("mark0025.json"),
            "marklhb": self._load_json_file("marklhb.json"),
            "marktheairei": self._load_json_file("marktheairei.json")
        }

        # Extract email accounts from LastPass
        self._extract_email_accounts(lastpass_creds)

    def _load_json_file(self, filename: str) -> Dict:
        file_path = self.credentials_path / filename
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            return {}

    def _extract_email_accounts(self, lastpass_creds: Dict):
        # Extract email accounts and their credentials
        for url, creds in lastpass_creds.items():
            if "@" in creds.get("username", ""):
                email = creds["username"]
                self.email_accounts[email] = {
                    "password": creds["password"],
                    "provider": self._determine_provider(email)
                }

    def _determine_provider(self, email: str) -> Dict:
        domain = email.split("@")[1]
        if "gmail" in domain:
            return {
                "imap_server": "imap.gmail.com",
                "smtp_server": "smtp.gmail.com"
            }
        elif "localhousebuyers" in domain:
            return {
                "imap_server": os.getenv("CUSTOM_IMAP_SERVER"),
                "smtp_server": os.getenv("CUSTOM_SMTP_SERVER")
            }
        # Add more providers as needed
        return {}

    def get_email_credentials(self, email: str) -> Dict:
        return self.email_accounts.get(email, {}) 