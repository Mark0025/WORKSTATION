from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from sqlalchemy import desc
from .models import TimelineEvent
import json

console = Console()

class TimelineLogger:
    def __init__(self, db_session):
        self.session = db_session
        self.log_dir = Path("timeline/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def save_log_to_file(self, events, filename=None):
        """Save events to markdown file"""
        if filename is None:
            filename = f"timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        log_file = self.log_dir / filename
        
        with open(log_file, 'w') as f:
            f.write("# Timeline Events Log\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for event in events:
                f.write(f"## {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"- Type: {event.event_type}\n")
                f.write(f"- Source: {event.source}\n")
                f.write(f"- Action: {event.action}\n")
                
                if event.details:
                    f.write("### Details\n```json\n")
                    f.write(json.dumps(event.details, indent=2))
                    f.write("\n```\n")
                
                if event.content:
                    f.write("### Content\n```\n")
                    f.write(event.content[:500] + ("..." if len(event.content) > 500 else ""))
                    f.write("\n```\n\n")
                
                f.write("---\n\n")
        
        return log_file

    def display_recent_changes(self, limit=100):
        """Display recent changes in rich table format"""
        events = self.session.query(TimelineEvent)\
            .order_by(desc(TimelineEvent.timestamp))\
            .limit(limit)\
            .all()
        
        # Create rich table
        table = Table(title=f"Recent Timeline Events (Last {limit})")
        table.add_column("Time", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Source", style="yellow", no_wrap=True)
        table.add_column("Action", style="magenta")
        table.add_column("Details", style="blue")
        
        for event in events:
            details = json.dumps(event.details, indent=2) if event.details else ""
            table.add_row(
                event.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                event.event_type,
                str(event.source)[:50] + "..." if event.source and len(event.source) > 50 else str(event.source),
                event.action,
                details[:50] + "..." if details and len(details) > 50 else details
            )
        
        # Save to file
        log_file = self.save_log_to_file(events)
        
        # Display in terminal
        console.print(table)
        console.print(f"\nLog saved to: {log_file}")
        
        return events

    def get_logs_by_type(self, event_type, limit=100):
        """Get logs filtered by event type"""
        return self.session.query(TimelineEvent)\
            .filter(TimelineEvent.event_type == event_type)\
            .order_by(desc(TimelineEvent.timestamp))\
            .limit(limit)\
            .all()

    def get_logs_by_source(self, source, limit=100):
        """Get logs filtered by source"""
        return self.session.query(TimelineEvent)\
            .filter(TimelineEvent.source.like(f"%{source}%"))\
            .order_by(desc(TimelineEvent.timestamp))\
            .limit(limit)\
            .all() 