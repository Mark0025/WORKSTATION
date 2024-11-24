import subprocess
import json
from datetime import datetime
from pathlib import Path
import re
from src.utils.file_utils import sanitize_filename, ensure_directory

class WisdomExtractor:
    def __init__(self):
        self.base_dir = Path("wisdom-ex")
        self.base_dir.mkdir(exist_ok=True)
        self.index_file = self.base_dir / "index.json"
        self.initialize_index()

    def initialize_index(self):
        """Initialize or load the index file"""
        if not self.index_file.exists():
            self.index_file.write_text(json.dumps({"projects": []}, indent=2))

    def get_video_info(self, url):
        """Get video title and author using fabric"""
        try:
            cmd = ["fabric", "-y", url, "--pattern", "video_info", "--stream"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                info = json.loads(result.stdout)
                return info.get('title', ''), info.get('author', 'unknown')
            return 'unknown', 'unknown'
        except:
            return 'unknown', 'unknown'

    def extract_wisdom(self, url):
        """Extract wisdom and organize into project structure"""
        try:
            title, author = self.get_video_info(url)
            date_str = datetime.now().strftime("%m-%d-%y")
            dir_name = sanitize_filename(f"{title}-{author}-{date_str}")
            project_dir = ensure_directory(self.base_dir / dir_name)

            cmd = ["fabric", "-y", url, "--pattern", "extract_wisdom", "--stream"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self._save_results(result.stdout, url, title, author, date_str, project_dir)
                return result.stdout, project_dir
            else:
                print(f"Error extracting wisdom: {result.stderr}")
                return None, None
        except Exception as e:
            print(f"Error running Fabric: {e}")
            return None, None

    def _save_results(self, wisdom_text, url, title, author, date_str, project_dir):
        """Save extraction results to files"""
        # Save wisdom text
        (project_dir / "wisdom.md").write_text(wisdom_text)
        
        # Save metadata
        metadata = {
            "title": title,
            "author": author,
            "date": date_str,
            "url": url,
            "extracted_date": datetime.now().isoformat()
        }
        
        (project_dir / "metadata.json").write_text(json.dumps(metadata, indent=2)) 