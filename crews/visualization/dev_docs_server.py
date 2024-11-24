from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from loguru import logger
import markdown
import uvicorn
from jinja2 import Template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from timeline.models import TimelineEvent
from fastapi.middleware.cors import CORSMiddleware
import sys
from timeline.logs.config import setup_logging
import requests
import psutil

# Setup logging
setup_logging("dev_docs")

# Create FastAPI app with /dev prefix
app = FastAPI(
    title="Development Documentation",
    docs_url="/dev/docs",
    openapi_url="/dev/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files under /dev prefix
app.mount("/dev/static", StaticFiles(directory="DEV-MAN"), name="static")
app.mount("/dev/diagrams", StaticFiles(directory="DEV-MAN/diagrams"), name="diagrams")

# HTML template
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
    <style>
        .sidebar {
            position: fixed;
            top: 0;
            bottom: 0;
            left: 0;
            padding: 20px;
            width: 250px;
            overflow-y: auto;
            background-color: #f8f9fa;
            border-right: 1px solid #dee2e6;
        }
        .main-content {
            margin-left: 250px;
            padding: 20px;
        }
        .diagram-container {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .card {
            transition: transform 0.2s;
            margin-bottom: 20px;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .card-icon {
            font-size: 2rem;
            margin-bottom: 15px;
            color: #0d6efd;
        }
        .stats {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .timeline-feed {
            max-width: 800px;
            margin: 0 auto;
        }
        .code-preview {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            font-size: 0.9em;
        }
        .badge {
            margin-left: 10px;
        }
        .details {
            font-size: 0.8em;
            color: #666;
        }
        .ai-interaction {
            border-left: 3px solid #0d6efd;
            padding-left: 10px;
        }
    </style>
    <script>
        // Global error handler
        window.onerror = function(msg, url, line, col, error) {
            fetch('/dev/log/error', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: msg,
                    url: url,
                    line: line,
                    column: col,
                    error: error?.stack,
                    userAgent: navigator.userAgent
                })
            });
            return false;
        };

        // Unhandled promise rejection handler
        window.addEventListener('unhandledrejection', function(event) {
            fetch('/dev/log/error', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: 'unhandledRejection',
                    reason: event.reason?.toString(),
                    stack: event.reason?.stack,
                    userAgent: navigator.userAgent
                })
            });
        });
    </script>
</head>
<body>
    <div class="sidebar">
        <h4>Documentation</h4>
        <hr>
        {{ navigation | safe }}
    </div>
    <div class="main-content">
        <h1>{{ title }}</h1>
        {{ content | safe }}
    </div>
    <script>
        mermaid.initialize({ startOnLoad: true });
    </script>
</body>
</html>
"""

def get_documentation_tree():
    """Get all documentation files"""
    dev_man = Path("DEV-MAN")
    docs = []
    
    # Get all markdown files
    for md_file in dev_man.rglob("*.md"):
        if md_file.is_file():
            docs.append({
                'path': md_file,
                'relative_path': md_file.relative_to(dev_man),
                'title': md_file.stem.replace('_', ' ').title()
            })
    
    return docs

def build_navigation(docs):
    """Build navigation HTML"""
    nav = ['<ul class="nav flex-column">']
    for doc in docs:
        nav.append(f'<li class="nav-item"><a class="nav-link" href="/dev/docs/{doc["relative_path"]}">{doc["title"]}</a></li>')
    nav.append('</ul>')
    return '\n'.join(nav)

@app.get("/dev", response_class=HTMLResponse)
async def index():
    """Main documentation page"""
    docs = get_documentation_tree()
    template = Template(PAGE_TEMPLATE)
    
    # Count different types of docs
    doc_counts = {
        'diagrams': len([d for d in docs if 'diagrams' in str(d['path'])]),
        'docs': len([d for d in docs if 'docs' in str(d['path'])]),
        'total': len(docs)
    }
    
    content = f"""
    <div class="container-fluid">
        <div class="row stats">
            <div class="col-md-4">
                <h3><i class="bi bi-file-text"></i> {doc_counts['docs']}</h3>
                <p>Documentation Files</p>
            </div>
            <div class="col-md-4">
                <h3><i class="bi bi-diagram-3"></i> {doc_counts['diagrams']}</h3>
                <p>Diagrams</p>
            </div>
            <div class="col-md-4">
                <h3><i class="bi bi-files"></i> {doc_counts['total']}</h3>
                <p>Total Files</p>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <div class="card-icon"><i class="bi bi-book"></i></div>
                        <h5 class="card-title">Documentation</h5>
                        <p class="card-text">View project documentation, guides, and best practices.</p>
                        <a href="/dev/docs" class="btn btn-primary">Browse Docs</a>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <div class="card-icon"><i class="bi bi-diagram-3"></i></div>
                        <h5 class="card-title">Diagrams</h5>
                        <p class="card-text">Explore project architecture and relationships.</p>
                        <a href="/dev/diagrams" class="btn btn-primary">View Diagrams</a>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <div class="card-icon"><i class="bi bi-gear"></i></div>
                        <h5 class="card-title">Project Setup</h5>
                        <p class="card-text">Learn how to set up and configure the project.</p>
                        <a href="/dev/docs/environment_management.md" class="btn btn-primary">Setup Guide</a>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <div class="card-icon"><i class="bi bi-box"></i></div>
                        <h5 class="card-title">Package Architecture</h5>
                        <p class="card-text">Understand the project's package structure.</p>
                        <a href="/dev/docs/project_architecture.md" class="btn btn-primary">View Architecture</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return template.render(
        title="Development Documentation",
        navigation=build_navigation(docs),
        content=content
    )

@app.get("/dev/docs/{path:path}", response_class=HTMLResponse)
async def get_doc(path: str):
    """Get specific documentation page"""
    try:
        file_path = Path("DEV-MAN") / path
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Document not found")
            
        # Read and convert markdown
        content = file_path.read_text()
        html_content = markdown.markdown(
            content,
            extensions=['fenced_code', 'tables', 'toc']
        )
        
        # Get all docs for navigation
        docs = get_documentation_tree()
        template = Template(PAGE_TEMPLATE)
        
        return template.render(
            title=file_path.stem.replace('_', ' ').title(),
            navigation=build_navigation(docs),
            content=html_content
        )
        
    except Exception as e:
        logger.error(f"Failed to serve document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dev/diagrams", response_class=HTMLResponse)
async def view_diagrams():
    """View all diagrams"""
    try:
        diagrams_dir = Path("DEV-MAN/diagrams")
        template = Template(PAGE_TEMPLATE)
        
        # Get all diagrams
        diagrams_content = []
        for file in diagrams_dir.glob("*.md"):
            if "viewer" not in file.name:
                content = file.read_text()
                if "```mermaid" in content:
                    diagrams_content.append({
                        'title': file.stem.replace('_', ' ').title(),
                        'content': content
                    })
        
        # Build content
        content = ['<div class="diagrams">']
        for diagram in diagrams_content:
            content.append(f'''
                <div class="diagram-container">
                    <h3>{diagram['title']}</h3>
                    {diagram['content']}
                </div>
            ''')
        content.append('</div>')
        
        docs = get_documentation_tree()
        return template.render(
            title="Project Diagrams",
            navigation=build_navigation(docs),
            content='\n'.join(content)
        )
        
    except Exception as e:
        logger.error(f"Failed to generate diagrams: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dev/timeline", response_class=HTMLResponse)
async def timeline_feed():
    """View activity timeline feed"""
    try:
        db_path = Path("timeline/data/timeline.db")
        if not db_path.exists():
            logger.error(f"Database not found at {db_path}")
            return template.render(
                title="Activity Timeline",
                navigation=build_navigation([]),
                content="<div class='alert alert-danger'>Database not found. Please run timeline watch first.</div>"
            )
            
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Get recent events
        events = session.query(TimelineEvent)\
            .order_by(TimelineEvent.timestamp.desc())\
            .limit(50)\
            .all()
            
        template = Template(PAGE_TEMPLATE)
        
        if not events:
            return template.render(
                title="Activity Timeline",
                navigation=build_navigation([]),
                content="<div class='alert alert-info'>No events recorded yet. Start making changes to see them here!</div>"
            )
            
        # Build timeline feed content
        content = ['<div class="timeline-feed">']
        for event in events:
            # Create card for each event
            content.append(f'''
                <div class="card mb-3">
                    <div class="card-header">
                        <i class="bi bi-clock"></i> {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
                        <span class="badge bg-primary">{event.event_type}</span>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">{event.source}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">{event.action}</h6>
                        
                        {f'<pre class="code-preview">{event.content[:200]}...</pre>' if event.content else ''}
                        
                        {f'<div class="details mt-2"><small>{json.dumps(event.details, indent=2)}</small></div>' if event.details else ''}
                        
                        {f'<div class="ai-interaction mt-2"><strong>AI Response:</strong><br>{event.ai_response[:200]}...</div>' if event.ai_response else ''}
                    </div>
                </div>
            ''')
        content.append('</div>')
        
        return template.render(
            title="Activity Timeline",
            navigation=build_navigation([]),
            content='\n'.join(content)
        )
        
    except Exception as e:
        logger.error(f"Failed to generate timeline: {str(e)}")
        return template.render(
            title="Activity Timeline",
            navigation=build_navigation([]),
            content=f"<div class='alert alert-danger'>Error: {str(e)}</div>"
        )

@app.get("/dev/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if we can read docs
        docs = get_documentation_tree()
        # Check if we can connect to database
        db_path = Path("timeline/data/timeline.db")
        if not db_path.exists():
            return {"status": "warning", "message": "Database not found"}
            
        return {
            "status": "healthy",
            "docs_count": len(docs),
            "database": "connected" if db_path.exists() else "missing"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}

@app.get("/dev/test")
async def test_endpoint():
    """Simple test endpoint"""
    logger.debug("Test endpoint called")
    return {"status": "ok", "message": "Dev docs server is running"}

# Add error logging middleware
@app.middleware("http")
async def log_errors(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Request failed: {request.url} - {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "path": str(request.url),
                "method": request.method
            }
        )

# Add JavaScript error logging endpoint
@app.post("/dev/log/error")
async def log_frontend_error(error: dict):
    """Log frontend errors"""
    logger.error(f"Frontend error: {error}")
    return {"status": "logged"}

@app.get("/dev/logs", response_class=HTMLResponse)
async def view_logs():
    """View application logs"""
    try:
        logs_dir = Path("timeline/logs")
        logs = []
        
        for log_file in logs_dir.glob("*.log"):
            with open(log_file) as f:
                logs.append({
                    'name': log_file.name,
                    'content': f.read().splitlines()[-1000:]  # Last 1000 lines
                })
        
        template = Template(PAGE_TEMPLATE)
        content = ['<div class="logs-viewer">']
        
        for log in logs:
            content.append(fr'''
                <div class="card mb-4">
                    <div class="card-header">
                        <h5>{log['name']}</h5>
                    </div>
                    <div class="card-body">
                        <pre class="log-content">{chr(10).join(log['content'])}</pre>
                    </div>
                </div>
            ''')
        
        content.append('</div>')
        
        return template.render(
            title="Application Logs",
            navigation=build_navigation([]),
            content='\n'.join(content)
        )
        
    except Exception as e:
        logger.error(f"Failed to display logs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dev/dashboard", response_class=HTMLResponse)
async def dashboard():
    """System monitoring dashboard"""
    try:
        # Get system stats
        import psutil
        
        # Get service status
        services = [
            {"name": "Timeline Watcher", "port": None},
            {"name": "Dev Docs Server", "port": 8010},
        ]
        
        for service in services:
            if service["port"]:
                try:
                    response = requests.get(f"http://localhost:{service['port']}/dev/health")
                    service["status"] = "🟢 Running" if response.status_code == 200 else "🔴 Error"
                except:
                    service["status"] = "🔴 Not Responding"
            else:
                service["status"] = "⚪️ Unknown"
        
        # Get database stats
        db_path = Path("timeline/data/timeline.db")
        if db_path.exists():
            engine = create_engine(f'sqlite:///{db_path}')
            with engine.connect() as conn:
                event_count = conn.execute("SELECT COUNT(*) FROM timeline_events").scalar()
        else:
            event_count = 0
            
        # Get log stats
        logs_dir = Path("timeline/logs")
        log_files = list(logs_dir.glob("*.log"))
        log_sizes = {log.name: f"{log.stat().st_size / 1024:.1f} KB" for log in log_files}
        
        template = Template(PAGE_TEMPLATE)
        content = f"""
        <div class="dashboard">
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>System Status</h5>
                        </div>
                        <div class="card-body">
                            <p>CPU: {psutil.cpu_percent()}%</p>
                            <p>Memory: {psutil.virtual_memory().percent}%</p>
                            <p>Disk: {psutil.disk_usage('/').percent}%</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Services</h5>
                        </div>
                        <div class="card-body">
                            {''.join(f"<p>{s['name']}: {s['status']}</p>" for s in services)}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Database</h5>
                        </div>
                        <div class="card-body">
                            <p>Events Recorded: {event_count}</p>
                            <p>Database Size: {db_path.stat().st_size / 1024:.1f} KB</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Logs</h5>
                        </div>
                        <div class="card-body">
                            {''.join(f"<p>{name}: {size}</p>" for name, size in log_sizes.items())}
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                // Auto-refresh every 30 seconds
                setTimeout(() => location.reload(), 30000);
            </script>
        </div>
        """
        
        return template.render(
            title="System Dashboard",
            navigation=build_navigation([]),
            content=content
        )
        
    except Exception as e:
        logger.error(f"Failed to generate dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Run the server"""
    try:
        logger.info("Starting dev docs server...")
        
        # 1. Verify docs directory exists
        docs_dir = Path("DEV-MAN")
        logger.debug(f"Looking for docs in: {docs_dir.absolute()}")
        if not docs_dir.exists():
            logger.error(f"DEV-MAN directory not found at {docs_dir.absolute()}")
            raise Exception("Documentation directory missing")
            
        # 2. Check documentation tree
        logger.info("Checking documentation tree...")
        docs = get_documentation_tree()
        logger.debug(f"Documentation files found: {[str(d['path']) for d in docs]}")
        
        # 3. Start server with detailed logging
        logger.info("Starting uvicorn server...")
        
        # Add debug mode and disable reloader for testing
        uvicorn.run(
            "crews.visualization.dev_docs_server:app",  # Use string path
            host="0.0.0.0", 
            port=8010,
            log_level="debug",
            reload=False  # Disable reload for testing
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.exception("Full traceback:")
        raise

if __name__ == "__main__":
    main() 