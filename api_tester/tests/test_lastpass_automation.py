import pytest
from loguru import logger
import aiohttp
import asyncio
from typing import Dict, Any

class LastPassAutomationTester:
    def __init__(self):
        self.logger = logger
        self.logger.add("logs/lastpass_automation.log")

    async def test_login_feasibility(self, credentials: Dict[str, Any]):
        """Test if automated login is feasible for a service"""
        try:
            async with aiohttp.ClientSession() as session:
                # First, check if the service has bot protection
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = await session.get(
                    credentials['url'],
                    headers=headers
                )
                
                # Check for common bot protection services
                security_headers = response.headers
                bot_protection = any(h in str(security_headers).lower() for h in [
                    'cloudflare',
                    'captcha',
                    'recaptcha',
                    'hcaptcha'
                ])

                return {
                    'url': credentials['url'],
                    'automation_feasible': not bot_protection,
                    'bot_protection': bot_protection,
                    'security_measures': [
                        h for h in security_headers 
                        if any(s in h.lower() for s in ['security', 'protection', 'csrf'])
                    ]
                }

        except Exception as e:
            self.logger.error(f"Error testing {credentials['url']}: {str(e)}")
            return {
                'url': credentials['url'],
                'error': str(e),
                'automation_feasible': False
            } 