from typing import Dict, Optional
from pydantic import BaseModel
import json
from pathlib import Path
from dotenv import load_dotenv
import os

class EmailCredentials(BaseModel):
    email: str
    password: str
    imap_server: str
    smtp_server: str
    api_credentials: Optional[Dict] = None

class CredentialsManager:
    def __init__(self):
        load_dotenv()
        self.credentials_path = Path("config/credentials")
        self.email_configs: Dict[str, EmailCredentials] = {}
        self.load_all_credentials()

    def load_all_credentials(self):
        # Load business-specific Google API credentials
        self.google_creds = {
            "personal": self._load_json_file("mark0025.json"),
            "lhb": self._load_json_file("marklhb.json"),
            "airei": self._load_json_file("marktheairei.json")
        }

        # Load LastPass credentials
        lastpass_creds = self._load_json_file("lastpass_credentials.json")
        
        # Map business emails to their configurations
        self._map_business_emails(lastpass_creds)

    def _map_business_emails(self, lastpass_creds: Dict):
        email_mappings = {
            "mark@localhousebuyers.net": {
                "business": "lhb",
                "api_creds": self.google_creds["lhb"]
            },
            "info@theairealestateinvestor.com": {
                "business": "airei",
                "api_creds": self.google_creds["airei"]
            },
            "markcarpenter0025@gmail.com": {
                "business": "personal",
                "api_creds": self.google_creds["personal"]
            }
        }

        for email, config in email_mappings.items():
            if email in lastpass_creds:
                self.email_configs[email] = EmailCredentials(
                    email=email,
                    password=lastpass_creds[email]["password"],
                    imap_server=self._get_imap_server(email),
                    smtp_server=self._get_smtp_server(email),
                    api_credentials=config["api_creds"]
                )

    def _get_imap_server(self, email: str) -> str:
        if "gmail.com" in email:
            return "imap.gmail.com"
        return os.getenv(f"{email.split('@')[1].upper()}_IMAP_SERVER")

    def _get_smtp_server(self, email: str) -> str:
        if "gmail.com" in email:
            return "smtp.gmail.com"
        return os.getenv(f"{email.split('@')[1].upper()}_SMTP_SERVER") 