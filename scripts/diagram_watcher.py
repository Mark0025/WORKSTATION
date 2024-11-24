from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jinja2 import Template
import time
from loguru import logger

class DiagramViewerUpdater(FileSystemEventHandler):
    def __init__(self):
        self.diagrams_dir = Path('DEV-MAN/diagrams')
        self.viewer_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Project Diagrams</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        .diagram-container {
            margin: 20px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .diagram-title {
            font-size: 24px;
            margin-bottom: 15px;
            color: #333;
        }
    </style>
    <script>
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose'
        });
    </script>
</head>
<body>
    <h1>Project Diagrams</h1>
    {% for diagram in diagrams %}
    <div class="diagram-container">
        <h2 class="diagram-title">{{ diagram.title }}</h2>
        <div class="mermaid">
            {{ diagram.content }}
        </div>
    </div>
    {% endfor %}
</body>
</html>
"""

    def update_viewer(self):
        """Update the viewer.html with all diagrams"""
        try:
            diagrams = []
            for file in self.diagrams_dir.glob('*.md'):
                if file.name != 'viewer.html':
                    content = file.read_text()
                    # Extract mermaid content
                    if '```mermaid' in content:
                        mermaid_content = content.split('```mermaid')[1].split('```')[0].strip()
                        diagrams.append({
                            'title': file.stem.replace('_', ' ').title(),
                            'content': mermaid_content
                        })
            
            # Render template
            template = Template(self.viewer_template)
            html = template.render(diagrams=diagrams)
            
            # Save viewer
            viewer_path = self.diagrams_dir / 'viewer.html'
            viewer_path.write_text(html)
            logger.success(f"Updated viewer with {len(diagrams)} diagrams")
            
        except Exception as e:
            logger.error(f"Failed to update viewer: {str(e)}")

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            logger.info(f"Diagram change detected: {event.src_path}")
            self.update_viewer()

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            logger.info(f"New diagram detected: {event.src_path}")
            self.update_viewer()

def watch_diagrams():
    """Start watching diagrams directory"""
    updater = DiagramViewerUpdater()
    
    # Do initial update
    updater.update_viewer()
    
    # Setup observer
    observer = Observer()
    observer.schedule(updater, str(updater.diagrams_dir), recursive=False)
    observer.start()
    
    try:
        logger.info(f"Started watching {updater.diagrams_dir}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_diagrams() 