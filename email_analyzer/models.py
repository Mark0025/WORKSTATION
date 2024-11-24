from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
from datetime import datetime

Base = declarative_base()

class EmailStatus(enum.Enum):
    INBOX = "inbox"
    SENT = "sent"
    NEEDS_DELETE = "needs_delete"
    DELETED = "deleted"

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    account = Column(String(255))  # Which email account it's from
    message_id = Column(String(255), unique=True)
    subject = Column(String(500))
    sender = Column(String(255))
    recipient = Column(String(255))
    date = Column(DateTime)
    body = Column(Text)
    status = Column(Enum(EmailStatus))
    folder = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 