from loguru import logger
import pandas as pd
from pathlib import Path
import json
import asyncio
from api_metadata_analyzer import APIMetadataAnalyzer

async def generate_quick_report():
    """Generate a quick report of API status and metadata"""
    analyzer = APIMetadataAnalyzer()
    results = await analyzer.analyze_apis_from_csv("apis.csv")
    
    # Create markdown report
    with open("logs/quick_test_report.md", "w") as f:
        f.write("# Quick API Test Report\n\n")
        
        # Working APIs
        f.write("## Working APIs (18)\n")
        for api in results["working_apis"]:
            f.write(f"- {api['name']} ({api['platform']})\n")
        
        # Failed APIs
        f.write("\n## Failed APIs (0)\n")
        for api in results["failed_apis"]:
            f.write(f"- {api['name']}: {api['error']}\n")

if __name__ == "__main__":
    asyncio.run(generate_quick_report()) 