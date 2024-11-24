import subprocess
import json
from datetime import datetime
from pathlib import Path
import re
from urllib.parse import urlparse, parse_qs

class WisdomExtractor:
    def __init__(self):
        self.base_dir = Path("wisdom-ex-library")
        self.base_dir.mkdir(exist_ok=True)
        self.index_file = self.base_dir / "index.json"
        self.initialize_index()

    def initialize_index(self):
        """Initialize or load the index file"""
        if not self.index_file.exists():
            self.index_file.write_text(json.dumps({"projects": []}, indent=2))

    def sanitize_filename(self, title):
        """Convert title to valid directory name"""
        return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')

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

    def extract_links(self, text):
        """Extract GitHub repos and other links from text"""
        github_pattern = r'https://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-_]+/?'
        general_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        
        github_links = re.findall(github_pattern, text)
        other_links = [link for link in re.findall(general_pattern, text) 
                      if link not in github_links]
        
        return {
            "github_repos": github_links,
            "other_links": other_links
        }

    def create_mermaid_diagram(self, title, resources):
        """Create a mermaid diagram of the project structure"""
        github_nodes = "\n".join(f"    C --> G{i}[{repo.split('/')[-1]}]" 
                                for i, repo in enumerate(resources['github_repos']))
        link_nodes = "\n".join(f"    D --> L{i}[Link {i+1}]" 
                              for i in range(len(resources['other_links'])))
        
        return f"""```mermaid
graph TD
    A[{title}] --> B[Resources]
    B --> C[GitHub Repos]
    B --> D[Other Links]
    B --> E[Wisdom Extract]
    {github_nodes}
    {link_nodes}
</file>