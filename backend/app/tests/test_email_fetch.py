import pytest
from app.core.credentials_manager import CredentialsManager
from app.services.email_service import EmailService

@pytest.fixture
def credentials_manager():
    return CredentialsManager()

@pytest.fixture
def email_service(credentials_manager):
    return EmailService(credentials_manager)

def test_fetch_emails_from_all_accounts(email_service):
    """Test fetching 5 emails from each business account"""
    test_emails = {
        "mark@localhousebuyers.net": 5,
        "info@theairealestateinvestor.com": 5,
        "markcarpenter0025@gmail.com": 5
    }
    
    for email, count in test_emails.items():
        emails = email_service.fetch_recent_emails(email, limit=count)
        assert len(emails) == count
        for email in emails:
            assert email.subject is not None
            assert email.sender is not None 