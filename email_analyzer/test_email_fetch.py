from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Email, EmailStatus
from credentials_manager import CredentialsManager
from fetcher import EmailFetcher
import os
from dotenv import load_dotenv
import asyncio
import imaplib
import email
from datetime import datetime
from typing import List, Dict, Any

class EmailAnalyzerTester:
    def __init__(self):
        # Set up logging
        logger.add("logs/email_analyzer.log", rotation="100 MB")
        
        # Load environment variables
        load_dotenv()
        
        # Initialize database
        db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
                 f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Initialize components
        self.creds_manager = CredentialsManager()

    async def fetch_emails(self, email_address: str, password: str, imap_server: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch emails from an account"""
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(email_address, password)
            
            emails = []
            
            # Check both INBOX and Sent folders
            for folder in ['INBOX', '[Gmail]/Sent Mail', '[Gmail]/Trash']:
                try:
                    mail.select(folder)
                    _, messages = mail.search(None, 'ALL')
                    email_ids = messages[0].split()[-limit:]  # Get last 5 emails
                    
                    for email_id in email_ids:
                        _, msg = mail.fetch(email_id, '(RFC822)')
                        email_body = msg[0][1]
                        message = email.message_from_bytes(email_body)
                        
                        # Parse email content
                        emails.append({
                            'account': email_address,
                            'message_id': message['Message-ID'],
                            'subject': message['subject'],
                            'sender': message['from'],
                            'recipient': message['to'],
                            'date': datetime.strptime(message['date'], '%a, %d %b %Y %H:%M:%S %z'),
                            'body': self._get_email_body(message),
                            'folder': folder,
                            'status': self._determine_status(folder)
                        })
                        
                except Exception as e:
                    logger.error(f"Error processing folder {folder}: {str(e)}")
                    continue
            
            return emails
            
        except Exception as e:
            logger.error(f"Error fetching emails from {email_address}: {str(e)}")
            return []

    def _get_email_body(self, message) -> str:
        """Extract email body from message"""
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return message.get_payload(decode=True).decode()

    def _determine_status(self, folder: str) -> EmailStatus:
        """Determine email status based on folder"""
        if folder == 'INBOX':
            return EmailStatus.INBOX
        elif folder == '[Gmail]/Sent Mail':
            return EmailStatus.SENT
        elif folder == '[Gmail]/Trash':
            return EmailStatus.NEEDS_DELETE
        return EmailStatus.INBOX

    async def run_test(self):
        """Test email fetching and storage"""
        try:
            # Test accounts from .env
            accounts = [
                {
                    'email': os.getenv('GMAIL_USERNAME'),
                    'password': os.getenv('GMAIL_APP_PASSWORD'),
                    'imap_server': 'imap.gmail.com'
                },
                {
                    'email': os.getenv('LHB_EMAIL'),
                    'password': os.getenv('LHB_PASSWORD'),
                    'imap_server': os.getenv('LHB_IMAP_SERVER')
                },
                {
                    'email': os.getenv('AIREI_EMAIL'),
                    'password': os.getenv('AIREI_PASSWORD'),
                    'imap_server': os.getenv('AIREI_IMAP_SERVER')
                }
            ]

            total_emails = 0
            
            for account in accounts:
                logger.info(f"Testing fetch for {account['email']}")
                
                # Fetch emails
                emails = await self.fetch_emails(
                    email_address=account['email'],
                    password=account['password'],
                    imap_server=account['imap_server']
                )
                
                # Store in database
                for email_data in emails:
                    email_obj = Email(**email_data)
                    self.session.add(email_obj)
                
                total_emails += len(emails)
                logger.info(f"Fetched {len(emails)} emails from {account['email']}")

            # Commit all changes
            self.session.commit()
            logger.success(f"Successfully stored {total_emails} emails in database")
            
        except Exception as e:
            logger.error(f"Error in email analyzer test: {str(e)}")
            self.session.rollback()
            raise
        finally:
            self.session.close()

if __name__ == "__main__":
    # Run the test
    tester = EmailAnalyzerTester()
    asyncio.run(tester.run_test()) 