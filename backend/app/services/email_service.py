from app.core.logger_config import logger
from app.core.credentials_manager import CredentialsManager
from typing import List, Dict
import imaplib
import email

class EmailService:
    def __init__(self, credentials_manager: CredentialsManager):
        self.credentials_manager = credentials_manager

    @logger.catch
    def fetch_recent_emails(self, email_address: str, limit: int = 5) -> List[Dict]:
        """
        Fetch recent emails with automatic error catching and logging
        """
        logger.info(f"Fetching {limit} emails for {email_address}")
        
        try:
            credentials = self.credentials_manager.get_email_credentials(email_address)
            
            if not credentials:
                logger.error(f"No credentials found for {email_address}")
                return []

            with imaplib.IMAP4_SSL(credentials.imap_server) as imap:
                logger.debug(f"Connecting to {credentials.imap_server}")
                imap.login(credentials.email, credentials.password)
                
                imap.select('INBOX')
                _, messages = imap.search(None, 'ALL')
                email_ids = messages[0].split()[-limit:]
                
                emails = []
                for email_id in email_ids:
                    try:
                        _, msg = imap.fetch(email_id, '(RFC822)')
                        email_body = msg[0][1]
                        email_message = email.message_from_bytes(email_body)
                        
                        email_data = {
                            'subject': email_message['subject'],
                            'from': email_message['from'],
                            'date': email_message['date']
                        }
                        emails.append(email_data)
                        logger.debug(f"Processed email: {email_data['subject']}")
                        
                    except Exception as e:
                        logger.exception(f"Error processing email {email_id}")
                        continue
                
                logger.success(
                    f"Successfully fetched {len(emails)} emails for {email_address}"
                )
                return emails
                
        except Exception as e:
            logger.exception(f"Failed to fetch emails for {email_address}")
            return [] 