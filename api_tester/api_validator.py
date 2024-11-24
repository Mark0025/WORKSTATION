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
        # Create logs directory if it doesn't exist
        Path("logs").mkdir(exist_ok=True)
        
        logger.add("logs/api_tests.log", 
                  rotation="100 MB",
                  format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
        
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
                        "key": key,  # Added to store in .env later
                        "status": status,
                        "working": 200 <= status < 300,
                        "error": None if 200 <= status < 300 else await response.text()
                    }
        except Exception as e:
            logger.error(f"Error testing {name} API: {str(e)}")
            return {
                "name": name,
                "key": key,
                "status": 500,
                "working": False,
                "error": str(e)
            } 