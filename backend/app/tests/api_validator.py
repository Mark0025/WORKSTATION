from loguru import logger
import requests
import json
from typing import Dict, Any, List
import csv
import os
from pathlib import Path
import aiohttp
import asyncio

class APIValidator:
    def __init__(self):
        logger.add("logs/api_tests.log", rotation="100 MB")
        self.api_endpoints = {
            "Open_AI": "https://api.openai.com/v1/models",
            "GO HIGH LEVEL": "https://rest.gohighlevel.com/v1/custom-values/",
            "Hugging Face": "https://huggingface.co/api/whoami",
            "SERP API": "https://serpapi.com/account",
            "Mail GUN": "https://api.mailgun.net/v3/domains",
            "Zapier": "https://nla.zapier.com/api/v1/exposed/",
            "Slack": "https://slack.com/api/auth.test",
            "ZOOM": "https://api.zoom.us/v2/users/me",
            "Docker": "https://hub.docker.com/v2/users/",
            "Github": "https://api.github.com/user",
            "Twilio": "https://api.twilio.com/2010-04-01/Accounts/",
            "Deepgram": "https://api.deepgram.com/v1/projects",
            "Weaviate": "https://test-tfvcklkt.weaviate.network/v1/schema"
        }

    async def test_api(self, name: str, key: str, endpoint: str) -> Dict[str, Any]:
        """Test an individual API endpoint"""
        headers = self._get_headers(name, key)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, headers=headers) as response:
                    status = response.status
                    logger.info(f"Testing {name} API: Status {status}")
                    return {
                        "name": name,
                        "status": status,
                        "working": 200 <= status < 300,
                        "error": None if 200 <= status < 300 else await response.text()
                    }
        except Exception as e:
            logger.error(f"Error testing {name} API: {str(e)}")
            return {
                "name": name,
                "status": 500,
                "working": False,
                "error": str(e)
            }

    def _get_headers(self, api_name: str, key: str) -> Dict[str, str]:
        """Get appropriate headers for each API"""
        headers = {
            "Open_AI": {"Authorization": f"Bearer {key}"},
            "GO HIGH LEVEL": {"Authorization": f"Bearer {key}"},
            "Hugging Face": {"Authorization": f"Bearer {key}"},
            "SERP API": {"Authorization": f"Bearer {key}"},
            "Mail GUN": {"Authorization": f"Basic {key}"},
            "Zapier": {"Authorization": f"Bearer {key}"},
            "Slack": {"Authorization": f"Bearer {key}"},
            "ZOOM": {"Authorization": f"Bearer {key}"},
            "Docker": {"Authorization": f"Bearer {key}"},
            "Github": {"Authorization": f"token {key}"},
            "Twilio": {"Authorization": f"Basic {key}"},
            "Deepgram": {"Authorization": f"Token {key}"},
            "Weaviate": {"Authorization": f"Bearer {key}"}
        }
        return headers.get(api_name, {"Authorization": f"Bearer {key}"})

    async def validate_all_apis(self, csv_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """Validate all APIs from CSV file"""
        working_apis = []
        failed_apis = []
        
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            tasks = []
            
            for row in reader:
                if row['Platform'] and row['API KEY']:
                    endpoint = self.api_endpoints.get(row['Platform'])
                    if endpoint:
                        task = self.test_api(row['Platform'], row['API KEY'], endpoint)
                        tasks.append(task)
                        
            results = await asyncio.gather(*tasks)
            
            for result in results:
                if result['working']:
                    working_apis.append(result)
                else:
                    failed_apis.append(result)
                    
        return {
            "working": working_apis,
            "failed": failed_apis
        }

    def generate_env_file(self, results: Dict[str, List[Dict[str, Any]]], output_path: str):
        """Generate .env file from working APIs"""
        with open(output_path, 'w') as env_file:
            env_file.write("# Working APIs\n")
            for api in results['working']:
                env_file.write(f"{api['name'].upper().replace(' ', '_')}_API_KEY={api['key']}\n")
                
            env_file.write("\n# Failed APIs - Need Investigation\n")
            for api in results['failed']:
                env_file.write(f"# {api['name']}: {api['error']}\n") 