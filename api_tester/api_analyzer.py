import pandas as pd
from loguru import logger
from typing import Dict, Any, List, Optional
import aiohttp
import asyncio
from pathlib import Path
import json
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, WebsiteSearchTool

class APIAnalyzer:
    def __init__(self):
        Path("logs").mkdir(exist_ok=True)
        logger.add("logs/api_analysis.log", rotation="100 MB")
        
        # Initialize research tools
        self.search_tool = SerperDevTool()
        self.web_tool = WebsiteSearchTool()
        
        # Known API configurations
        self.api_configs = {
            "Open_AI": {
                "endpoint": "https://api.openai.com/v1/models",
                "test_payload": None,
                "auth_type": "Bearer",
                "docs_url": "https://platform.openai.com/docs/api-reference"
            },
            "GO HIGH LEVEL": {
                "endpoint": "https://rest.gohighlevel.com/v1/custom-values/",
                "auth_type": "Bearer",
                "docs_url": "https://highlevel.stoplight.io/docs/integrations/"
            },
            "Hugging Face": {
                "endpoint": "https://huggingface.co/api/whoami",
                "auth_type": "Bearer",
                "docs_url": "https://huggingface.co/docs/api-inference/index"
            }
            # Add more API configurations as needed
        }

    async def analyze_apis_from_csv(self, csv_path: str) -> Dict[str, Any]:
        """Analyze APIs from CSV file using pandas"""
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Found {len(df)} API entries in CSV")
            
            # Initialize results
            analysis = {
                "working_apis": [],
                "unknown_apis": [],
                "invalid_apis": [],
                "needs_investigation": []
            }
            
            for _, row in df.iterrows():
                result = await self._analyze_api_entry(row)
                category = result.pop("category")
                analysis[category].append(result)
            
            # Generate reports
            self._generate_env_files(analysis)
            self._generate_analysis_report(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing APIs: {str(e)}")
            raise

    async def _analyze_api_entry(self, row: pd.Series) -> Dict[str, Any]:
        """Analyze individual API entry"""
        name = row.get("Name", "Unknown")
        api_key = row.get("API KEY")
        platform = row.get("Platform")
        
        if not api_key:
            return {
                "name": name,
                "category": "invalid_apis",
                "reason": "No API key provided"
            }
        
        # Check if we know how to handle this API
        if platform in self.api_configs:
            config = self.api_configs[platform]
            test_result = await self._test_api(platform, api_key, config)
            return {
                "name": name,
                "platform": platform,
                "key": api_key,
                "category": "working_apis" if test_result["working"] else "invalid_apis",
                "status": test_result.get("status"),
                "error": test_result.get("error")
            }
        else:
            # Use CrewAI to investigate unknown API
            investigation = await self._investigate_unknown_api(name, platform)
            return {
                "name": name,
                "platform": platform,
                "key": api_key,
                "category": "needs_investigation",
                "investigation_result": investigation
            }

    def _generate_env_files(self, analysis: Dict[str, List[Dict[str, Any]]]):
        """Generate .env files for working and non-working APIs"""
        # Working APIs
        with open('.env.working', 'w') as f:
            f.write("# Working APIs\n\n")
            for api in analysis["working_apis"]:
                key_name = f"{api['platform'].upper().replace(' ', '_')}_API_KEY"
                f.write(f"{key_name}={api['key']}\n")
        
        # Non-working APIs
        with open('.env.not-working', 'w') as f:
            f.write("# Non-working APIs\n\n")
            for category in ["invalid_apis", "needs_investigation"]:
                f.write(f"\n# {category.replace('_', ' ').title()}\n")
                for api in analysis[category]:
                    key_name = f"{api.get('platform', 'UNKNOWN').upper().replace(' ', '_')}_API_KEY"
                    f.write(f"# {key_name}={api['key']} # Reason: {api.get('reason', 'Unknown')}\n")

    async def _investigate_unknown_api(self, name: str, platform: str) -> Dict[str, Any]:
        """Use CrewAI to investigate unknown APIs"""
        researcher = Agent(
            role="API Researcher",
            goal="Investigate and understand unknown APIs",
            tools=[self.search_tool, self.web_tool]
        )
        
        investigation_task = Task(
            description=f"Research the API: {name} ({platform}). Find documentation and usage information.",
            agent=researcher
        )
        
        crew = Crew(
            agents=[researcher],
            tasks=[investigation_task]
        )
        
        result = await crew.kickoff()
        return result

    def _generate_analysis_report(self, analysis: Dict[str, List[Dict[str, Any]]]):
        """Generate detailed analysis report"""
        report_path = Path("logs/api_analysis_report.md")
        
        with open(report_path, 'w') as report:
            report.write("# API Analysis Report\n\n")
            
            # Working APIs
            report.write("## Working APIs\n")
            for api in analysis["working_apis"]:
                report.write(f"### {api['name']}\n")
                report.write(f"- Platform: {api['platform']}\n")
                report.write(f"- Status: {api['status']}\n\n")
            
            # Unknown APIs
            report.write("## APIs Needing Investigation\n")
            for api in analysis["needs_investigation"]:
                report.write(f"### {api['name']}\n")
                report.write(f"- Platform: {api['platform']}\n")
                report.write(f"- Investigation Results: {api['investigation_result']}\n\n") 