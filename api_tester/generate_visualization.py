from config.naming_standards import APINameStandards
import json
from pathlib import Path
from loguru import logger
import pandas as pd

class APIVisualizer:
    def __init__(self):
        self.standards = APINameStandards()
        self.visualization_dir = Path("visualization")
        self.visualization_dir.mkdir(exist_ok=True)

    def generate_mermaid_diagram(self, api_data: dict) -> str:
        """Generate Mermaid.js diagram"""
        diagram = ["graph TD"]
        
        # Add subgraphs for each category
        for category, apis in self.standards.PLATFORM_CATEGORIES.items():
            diagram.append(f"    subgraph {category}")
            for api in apis:
                status = api_data.get(api, {}).get("status", "unknown")
                color = self.standards.get_status_color(status)
                diagram.append(f"        {api}[{api}]:::status_{status}")
            diagram.append("    end")
        
        # Add connections
        diagram.extend([
            "    OpenAI --> CrewAI",
            "    SERP-API --> CrewAI",
            "    GoHighLevel --> MailGun",
            "    Weaviate --> OpenAI",
            "    HuggingFace --> AutoGen"
        ])
        
        # Add styling
        diagram.extend([
            "    classDef status_active fill:#10B981,stroke:#047857",
            "    classDef status_inactive fill:#EF4444,stroke:#B91C1C",
            "    classDef status_pending fill:#F59E0B,stroke:#B45309",
            "    classDef status_unknown fill:#6B7280,stroke:#374151"
        ])
        
        return "\n".join(diagram)

    def generate_html(self, api_data: dict):
        """Generate HTML visualization"""
        mermaid_diagram = self.generate_mermaid_diagram(api_data)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Ecosystem Visualization</title>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto px-4 py-8">
                <h1 class="text-4xl font-bold mb-8">API Ecosystem Status</h1>
                
                <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
                    <div class="mermaid">
                    {mermaid_diagram}
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {self._generate_status_cards(api_data)}
                </div>
            </div>
            
            <script>
                mermaid.initialize({{
                    'startOnLoad': true,
                    'theme': 'default',
                    'securityLevel': 'loose'
                }});
            </script>
        </body>
        </html>
        """
        
        with open(self.visualization_dir / "api_ecosystem.html", "w") as f:
            f.write(html_content)

    def _generate_status_cards(self, api_data: dict) -> str:
        """Generate status cards HTML"""
        cards = []
        for status in ["active", "inactive", "pending"]:
            apis = [name for name, data in api_data.items() 
                   if data.get("status") == status]
            
            color = self.standards.get_status_color(status)
            cards.append(f"""
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-xl font-semibold mb-4" style="color: {color}">
                        {status.title()} APIs ({len(apis)})
                    </h2>
                    <ul class="space-y-2">
                        {''.join(f'<li>{api}</li>' for api in apis)}
                    </ul>
                </div>
            """)
        
        return "\n".join(cards)

if __name__ == "__main__":
    visualizer = APIVisualizer()
    # Read API data from test results
    with open("logs/quick_test_report.md") as f:
        # Parse the markdown to get API data
        # This is a simplified example
        api_data = {}  # You'll need to implement the parsing
    visualizer.generate_html(api_data) 