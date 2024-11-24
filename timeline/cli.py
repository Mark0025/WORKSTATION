import click
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .logs import TimelineLogger
from .analyzer_crew import TimelineAnalyzerCrew
from .watcher import TimelineEventHandler
from watchdog.observers import Observer
import time
from pathlib import Path
from loguru import logger

console = Console()

@click.group()
def cli():
    """Timeline - Track your development activity"""
    pass

@cli.command()
@click.option('--path', default='.', help='Path to watch')
@click.option('--db', default='sqlite:///timeline/data/timeline.db', help='Database URL')
def watch(path, db):
    """Watch directory for changes"""
    try:
        # Initialize database if it doesn't exist
        if not Path("timeline/data/timeline.db").exists():
            logger.info("Database not found, initializing...")
            from .init_db import init_database
            init_database()
        
        logger.info(f"Starting watcher with db: {db}")
        engine = create_engine(db)
        logger.info("Created engine")
        
        Session = sessionmaker(bind=engine)
        session = Session()
        logger.info("Created session")
        
        event_handler = TimelineEventHandler(session)
        logger.info("Created event handler")
        
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        logger.info(f"Scheduled observer for path: {path}")
        
        observer.start()
        logger.info("Observer started")
        
        console.print(f"[green]Started watching {Path(path).absolute()}[/green]")
        while True:
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"Watch failed: {str(e)}")
        raise
    finally:
        if 'observer' in locals():
            observer.stop()
            observer.join()

@cli.command()
@click.option('--limit', default=100, help='Number of events to show')
@click.option('--type', help='Filter by event type')
@click.option('--source', help='Filter by source')
@click.option('--db', default='sqlite:///timeline.db', help='Database URL')
def logs(limit, type, source, db):
    """Show recent timeline events with filtering options"""
    engine = create_engine(db)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    logger = TimelineLogger(session)
    
    if type:
        events = logger.get_logs_by_type(type, limit)
    elif source:
        events = logger.get_logs_by_source(source, limit)
    else:
        events = logger.display_recent_changes(limit)
    
    if not events:
        console.print("[yellow]No events found matching criteria[/yellow]")

@cli.command()
@click.option('--days', default=7, help='Days of history to analyze')
@click.option('--db', default='sqlite:///timeline.db', help='Database URL')
def analyze(days, db):
    """Analyze timeline and suggest improvements"""
    engine = create_engine(db)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    analyzer = TimelineAnalyzerCrew()
    result = analyzer.analyze_timeline(days_back=days)
    
    console.print("[green]Analysis complete![/green]")
    console.print(result)

def main():
    cli()

if __name__ == "__main__":
    main() 