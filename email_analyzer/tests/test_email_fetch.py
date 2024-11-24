import os
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from email_analyzer.models.email_model import Base, Email, EmailStatus
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import asyncio
import imaplib
import email
from datetime import datetime

class EmailTester:
    def __init__(self):
        # Set up logging
        logger.add("email_analyzer/logs/email_test.log", rotation="100 MB")
        
        # Load environment variables
        load_dotenv()
        
        # Initialize database
        self.setup_database()

    def setup_database(self):
        """Setup database connection"""
        try:
            db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
                     f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
            
            self.engine = create_engine(db_url)
            Base.metadata.create_all(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise

    async def test_email_accounts(self):
        """Test email fetching from all configured accounts"""
        accounts = [
            {
                'name': 'Gmail',
                'email': os.getenv('GMAIL_USERNAME'),
                'password': os.getenv('GMAIL_APP_PASSWORD'),
                'server': 'imap.gmail.com'
            },
            {
                'name': 'LHB',
                'email': os.getenv('LHB_EMAIL'),
                'password': os.getenv('LHB_PASSWORD'),
                'server': os.getenv('LHB_IMAP_SERVER')
            },
            {
                'name': 'AIREI',
                'email': os.getenv('AIREI_EMAIL'),
                'password': os.getenv('AIREI_PASSWORD'),
                'server': os.getenv('AIREI_IMAP_SERVER')
            }
        ]

        for account in accounts:
            try:
                logger.info(f"Testing {account['name']} account...")
                await self.fetch_emails(account)
            except Exception as e:
                logger.error(f"Error testing {account['name']}: {str(e)}")

    async def fetch_emails(self, account: dict, limit: int = 5):
        """Fetch emails from an account"""
        try:
            mail = imaplib.IMAP4_SSL(account['server'])
            mail.login(account['email'], account['password'])
            
            for folder in ['INBOX', 'Sent', 'Trash']:
                try:
                    mail.select(folder)
                    _, messages = mail.search(None, 'ALL')
                    email_ids = messages[0].split()[-limit:]
                    
                    for email_id in email_ids:
                        _, msg = mail.fetch(email_id, '(RFC822)')
                        email_msg = email.message_from_bytes(msg[0][1])
                        
                        email_obj = Email(
                            account=account['email'],
                            message_id=email_msg['Message-ID'],
                            subject=email_msg['subject'],
                            sender=email_msg['from'],
                            recipient=email_msg['to'],
                            date=datetime.now(),  # You might want to parse the actual date
                            body=self._get_email_body(email_msg),
                            status=EmailStatus.INBOX,
                            folder=folder
                        )
                        
                        self.session.add(email_obj)
                        logger.info(f"Stored email: {email_obj.subject}")
                        
                except Exception as e:
                    logger.error(f"Error processing folder {folder}: {str(e)}")
                    continue
                    
            self.session.commit()
            logger.success(f"Successfully processed emails for {account['name']}")
            
        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}")
            self.session.rollback()
            raise

    def _get_email_body(self, message) -> str:
        """Extract email body from message"""
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return message.get_payload(decode=True).decode()

def main():
    tester = EmailTester()
    asyncio.run(tester.test_email_accounts())

if __name__ == "__main__":
    main() 