from pathlib import Path
from sqlalchemy import create_engine
from loguru import logger
from .models import Base

def init_database():
    """Initialize the SQLite database"""
    try:
        # Create database directory if it doesn't exist
        db_dir = Path("timeline/data")
        db_dir.mkdir(parents=True, exist_ok=True)
        
        # Create database
        db_path = db_dir / "timeline.db"
        engine = create_engine(f'sqlite:///{db_path}')
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        logger.success(f"Database initialized at {db_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return False

if __name__ == "__main__":
    init_database() 