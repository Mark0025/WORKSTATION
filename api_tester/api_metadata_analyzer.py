import pandas as pd
from pathlib import Path
import json
from typing import Dict, Any, List
import glob
from loguru import logger
import mermaid_diagram as mm

class APIMetadataAnalyzer:
    def __init__(self):
        self.api_metadata = {
            "Open_AI": {
                "description": "OpenAI's API for AI models and services",
                "use_cases": ["Text Generation", "Code Assistance", "Chat", "Embeddings"],
                "models": {
                    "gpt-4": {
                        "token_limit": 8192,
                        "cost_per_1k_tokens": "$0.03/$0.06",
                        "best_for": "Complex reasoning, coding"
                    },
                    "gpt-3.5-turbo": {
                        "token_limit": 4096,
                        "cost_per_1k_tokens": "$0.0015/$0.002",
                        "best_for": "General purpose, chat"
                    }
                },
                "pros": [
                    "State-of-the-art models",
                    "Extensive documentation",
                    "High reliability"
                ],
                "cons": [
                    "Can be expensive at scale",
                    "Rate limits on free tier",
                    "Token limitations"
                ]
            },
            "GO HIGH LEVEL": {
                "description": "All-in-one marketing and CRM platform",
                "use_cases": ["CRM", "Marketing Automation", "Lead Management"],
                "pros": ["Comprehensive feature set", "Good API documentation"],
                "cons": ["Complex integration", "Learning curve"]
            },
            "SERP API": {
                "description": "Search engine results scraping API",
                "use_cases": ["SEO Research", "Market Analysis", "Content Research"],
                "pros": ["Reliable data", "Multiple search engines"],
                "cons": ["Usage-based pricing", "Rate limits"]
            }
            # Add more API metadata as needed
        }

    def generate_mermaid_diagram(self, api_data: Dict[str, Any]) -> str:
        """Generate Mermaid.js diagram showing API architecture"""
        diagram = """
graph TD
    subgraph AI_Services[AI Services]
        OpenAI[OpenAI API]
        HuggingFace[Hugging Face]
        Claude[Claude]
    end

    subgraph Marketing_Tools[Marketing & CRM]
        GHL[Go High Level]
        MailGun[Mail Gun]
    end

    subgraph Search_Tools[Search & Research]
        SERP[SERP API]
        Google[Google Search]
    end

    subgraph Development_Tools[Development Tools]
        GitHub[GitHub]
        Docker[Docker]
    end
"""
        # Add status colors and connections
        for api_name, api_info in api_data.items():
            status_color = self._get_status_color(api_info["status"])
            diagram += f"    {api_name}[{api_name}]:::status_{status_color}\n"

        return diagram

    def _get_status_color(self, status: str) -> str:
        """Get color based on API status"""
        color_map = {
            "working": "green",
            "inactive": "grey",
            "failed": "red",
            "unknown": "yellow"
        }
        return color_map.get(status, "yellow")

    def analyze_all_env_files(self) -> Dict[str, Any]:
        """Analyze all .env files in the workspace"""
        env_files = glob.glob("**/.env*", recursive=True)
        combined_data = {}

        for env_file in env_files:
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        combined_data[key] = {
                            "value": value,
                            "source_file": env_file
                        }

        return combined_data

    def generate_api_report(self) -> Dict[str, Any]:
        """Generate comprehensive API report with metadata"""
        report = {
            "apis": {},
            "statistics": {
                "total_apis": 0,
                "working_apis": 0,
                "failed_apis": 0,
                "unknown_apis": 0
            }
        }

        # Read CSV data
        df = pd.read_csv("apis.csv")
        
        for _, row in df.iterrows():
            api_name = row.get("Name")
            platform = row.get("Platform")
            
            api_info = {
                "platform": platform,
                "key": row.get("API KEY"),
                "status": self._check_api_status(row),
                "metadata": self.api_metadata.get(platform, {}),
                "additional_info": {
                    "engine": row.get("Engine"),
                    "callback_url": row.get("CALL BACK URL"),
                    "id": row.get("ID")
                }
            }
            
            report["apis"][api_name] = api_info
            report["statistics"]["total_apis"] += 1
            report["statistics"][f"{api_info['status']}_apis"] += 1

        return report

    def _check_api_status(self, api_data: pd.Series) -> str:
        """Determine API status based on our tests and metadata"""
        # Implementation would check against our test results
        return "working"  # Placeholder

    def save_visualization(self, report: Dict[str, Any]):
        """Save visualization of API architecture"""
        diagram = self.generate_mermaid_diagram(report["apis"])
        
        with open("api_architecture.md", "w") as f:
            f.write("# API Architecture\n\n")
            f.write("```mermaid\n")
            f.write(diagram)
            f.write("\n```\n") 