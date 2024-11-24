from .models import TimelineEvent, CursorEventType
from sqlalchemy.orm import Session
from loguru import logger
import json

class CursorEventHandler:
    def __init__(self, db_session: Session):
        self.session = db_session
        
    def record_cursor_event(self, 
                           event_type: CursorEventType,
                           user_input: str = None,
                           ai_response: str = None,
                           code_changes: dict = None,
                           file_path: str = None):
        """Record a Cursor IDE event"""
        try:
            event = TimelineEvent(
                event_type='cursor',
                source=file_path or 'cursor',
                action=event_type.value,
                cursor_event_type=event_type,
                user_input=user_input,
                ai_response=ai_response,
                code_changes=code_changes,
                details={
                    'cursor_version': '0.1',  # Add version tracking
                    'has_code_changes': bool(code_changes),
                    'files_affected': list(code_changes.keys()) if code_changes else []
                }
            )
            
            self.session.add(event)
            self.session.commit()
            logger.info(f"Recorded Cursor {event_type.value} event")
            
        except Exception as e:
            logger.error(f"Failed to record Cursor event: {str(e)}")
            raise 