import imaplib
import email
from datetime import datetime
from email_analyzer.database import SessionLocal, Email
from config.settings import EMAIL_ACCOUNTS
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailFetcher:
    def __init__(self, account_name: str = "primary"):
        self.credentials = EMAIL_ACCOUNTS[account_name]
        self.session = SessionLocal()

    def connect(self) -> imaplib.IMAP4_SSL:
        mail = imaplib.IMAP4_SSL(self.credentials["imap_server"])
        mail.login(self.credentials["username"], self.credentials["password"])
        return mail

    def fetch_emails(self, limit: int = 100) -> List[Dict]:
        try:
            mail = self.connect()
            mail.select('inbox')
            
            _, messages = mail.search(None, 'ALL')
            email_ids = messages[0].split()[-limit:]  # Get last 'limit' emails
            
            emails = []
            for email_id in email_ids:
                _, msg = mail.fetch(email_id, '(RFC822)')
                email_body = msg[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Extract email data
                email_data = {
                    'subject': email_message['subject'],
                    'sender': email_message['from'],
                    'recipient': email_message['to'],
                    'date': datetime.strptime(email_message['date'], '%a, %d %b %Y %H:%M:%S %z'),
                    'content': self._get_email_content(email_message)
                }
                
                # Save to database
                self._save_to_db(email_data)
                emails.append(email_data)
            
            return emails
            
        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}")
            raise
        finally:
            mail.logout()

    def _get_email_content(self, email_message) -> str:
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return email_message.get_payload(decode=True).decode()

    def _save_to_db(self, email_data: Dict) -> None:
        db_email = Email(**email_data)
        self.session.add(db_email)
        self.session.commit() 