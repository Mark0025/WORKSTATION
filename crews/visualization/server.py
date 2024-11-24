from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from loguru import logger
import uvicorn
from .. import BaseCrew

app = FastAPI(title="CrewAI Visualizations")

# Mount static files
app.mount("/static", StaticFiles(directory="crews/crew-output"), name="static")

@app.get("/", response_class=HTMLResponse)
async def view_diagrams():
    """Display all Mermaid diagrams from crew outputs"""
    try:
        # Get all diagram files
        output_dir = Path("crews/crew-output")
        diagram_files = list(output_dir.glob("**/*_diagram_*.md"))
        
        # Build HTML with all diagrams
        diagrams_html = ""
        for file in diagram_files:
            with open(file) as f:
                content = f.read()
                diagrams_html += f"""
                <div class="diagram-container">
                    <h3>{file.stem}</h3>
                    {content}
                </div>
                """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CrewAI Visualizations</title>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <style>
                .diagram-container {{
                    margin: 20px;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <h1>CrewAI Visualizations</h1>
            {diagrams_html}
            <script>
                mermaid.initialize({{ startOnLoad: true }});
            </script>
        </body>
        </html>
        """
    except Exception as e:
        logger.error(f"Failed to generate visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 