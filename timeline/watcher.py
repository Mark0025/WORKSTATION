from watchdog.events import FileSystemEventHandler
from pathlib import Path
from datetime import datetime
import json
from .models import TimelineEvent
from sqlalchemy.orm import Session
from loguru import logger

class TimelineEventHandler(FileSystemEventHandler):
    def __init__(self, db_session: Session, ignored_patterns=None):
        self.session = db_session
        self.ignored_patterns = ignored_patterns or [
            '*.pyc', '__pycache__', '.git', 'node_modules',
            '*.swp', '*.swo', '.DS_Store'
        ]
        
    def should_ignore(self, path):
        path_str = str(path)
        return any(pattern in path_str for pattern in self.ignored_patterns)
        
    def on_modified(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
            
        try:
            path = Path(event.src_path)
            
            # Create timeline event
            timeline_event = TimelineEvent(
                event_type='file_change',
                source=str(path),
                action='modified',
                details={
                    'size': path.stat().st_size,
                    'extension': path.suffix,
                    'directory': str(path.parent)
                },
                content=path.read_text()[:1000] if path.is_file() else None
            )
            
            self.session.add(timeline_event)
            self.session.commit()
            logger.info(f"Recorded modification to {path}")
            
        except Exception as e:
            logger.error(f"Failed to record event: {str(e)}") 