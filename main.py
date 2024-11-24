from email_analyzer.fetcher import EmailFetcher
from email_analyzer.analyst import EmailAnalyst
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Fetch emails
        fetcher = EmailFetcher()
        fetcher.fetch_emails(limit=100)
        logger.info("Emails fetched successfully")
        
        # Analyze emails
        analyst = EmailAnalyst()
        results = analyst.analyze_emails(limit=10)
        logger.info(f"Analyzed {len(results)} emails")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main() 