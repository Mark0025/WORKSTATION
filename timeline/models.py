from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class CursorEventType(enum.Enum):
    CHAT = "chat"
    COMPOSE = "compose"
    CREATE = "create"
    EDIT = "edit"
    COMMAND = "command"
    SUGGESTION = "suggestion"

class TimelineEvent(Base):
    __tablename__ = 'timeline_events'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String(50))  # 'file_change', 'cursor', 'terminal'
    source = Column(String(100))     # File path or source
    action = Column(String(50))      # Action type
    details = Column(JSON)           # Additional details
    content = Column(Text)           # Event content
    
    # Cursor-specific fields
    cursor_event_type = Column(Enum(CursorEventType), nullable=True)
    ai_response = Column(Text, nullable=True)        # AI's response
    user_input = Column(Text, nullable=True)         # User's input
    code_changes = Column(JSON, nullable=True)       # Code changes made 