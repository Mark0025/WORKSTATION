import pty
import os
import sys
from .models import TimelineEvent
from sqlalchemy.orm import Session

def capture_terminal(db_session: Session):
    """Capture terminal commands"""
    def read(fd):
        data = os.read(fd, 1024)
        if data:
            # Record command in timeline
            event = TimelineEvent(
                event_type='terminal',
                source='shell',
                action='command',
                content=data.decode()
            )
            db_session.add(event)
            db_session.commit()
        return data

    pty.spawn("/bin/bash", read) 