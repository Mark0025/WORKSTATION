from pathlib import Path
import re

def sanitize_filename(title):
    """Convert title to valid directory name"""
    return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')

def ensure_directory(path):
    """Ensure directory exists and return Path object"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path 