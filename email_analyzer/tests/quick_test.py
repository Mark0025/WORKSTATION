from loguru import logger
import json
from pathlib import Path
import imaplib
import email
from email.header import decode_header
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GmailTester:
    def __init__(self):
        self.creds_dir = Path("config/credentials")
        logger.add("email_analyzer/logs/email_test.log")

    def load_credentials(self, json_file: str):
        """Load OAuth credentials from JSON file"""
        try:
            creds_path = self.creds_dir / json_file
            logger.info(f"Loading credentials from {json_file}")
            
            with open(creds_path) as f:
                cred_data = json.load(f)
                
            # Use installed credentials from JSON
            flow = InstalledAppFlow.from_client_config(
                cred_data,
                ['https://www.googleapis.com/auth/gmail.readonly']
            )
            
            return flow.run_local_server(port=0)
            
        except Exception as e:
            logger.error(f"Error loading credentials from {json_file}: {str(e)}")
            raise

    async def test_email_accounts(self):
        """Test Gmail accounts using OAuth credentials"""
        accounts = [
            {
                'name': 'Gmail',
                'json_file': 'mark0025.json'
            },
            {
                'name': 'LHB',
                'json_file': 'marklhb.json'
            },
            {
                'name': 'AIREI',
                'json_file': 'marktheairei.json'
            }
        ]

        for account in accounts:
            try:
                logger.info(f"\nTesting {account['name']} account...")
                
                # Load OAuth credentials
                creds = self.load_credentials(account['json_file'])
                
                # Use credentials to fetch emails
                service = build('gmail', 'v1', credentials=creds)
                results = service.users().messages().list(userId='me', maxResults=5).execute()
                messages = results.get('messages', [])

                logger.success(f"Successfully connected to {account['name']}")
                logger.info(f"Fetching last 5 emails...")

                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    headers = msg['payload']['headers']
                    
                    subject = next(h['value'] for h in headers if h['name'] == 'Subject')
                    sender = next(h['value'] for h in headers if h['name'] == 'From')
                    date = next(h['value'] for h in headers if h['name'] == 'Date')
                    
                    logger.info(f"Subject: {subject}")
                    logger.info(f"From: {sender}")
                    logger.info(f"Date: {date}\n")

            except Exception as e:
                logger.error(f"Error with {account['name']}: {str(e)}")

if __name__ == "__main__":
    # Install required packages
    import subprocess
    subprocess.run(["uv", "pip", "install", "google-auth-oauthlib", "google-auth-httplib2", "google-api-python-client"])
    
    # Run tests
    tester = GmailTester()
    import asyncio
    asyncio.run(tester.test_email_accounts())
