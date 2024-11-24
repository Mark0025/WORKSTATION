import asyncio
import aiohttp
from loguru import logger
import pandas as pd
from pathlib import Path
import json

class QuickAPITester:
    def __init__(self):
        logger.add("logs/quick_test.log")
        
        # Define test cases for different API types
        self.test_cases = {
            "Open_AI": {
                "url": "https://api.openai.com/v1/chat/completions",
                "payload": {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Tell me a short joke"}]
                }
            },
            "SERP API": {
                "url": "https://serpapi.com/search",
                "params": {
                    "q": "test query",
                    "engine": "google"
                }
            },
            "GO HIGH LEVEL": {
                "url": "https://rest.gohighlevel.com/v1/contacts/",
                "method": "GET"
            }
        }

    async def test_api(self, name: str, key: str, platform: str):
        """Quick test of a single API"""
        try:
            if platform not in self.test_cases:
                return {"status": "unknown", "message": f"No test case for {platform}"}

            test_case = self.test_cases[platform]
            headers = {"Authorization": f"Bearer {key}"}

            async with aiohttp.ClientSession() as session:
                if platform == "Open_AI":
                    async with session.post(test_case["url"], json=test_case["payload"], headers=headers) as response:
                        result = await response.json()
                        logger.info(f"OpenAI response: {result}")
                        return {"status": "working", "response": result}

                elif platform == "SERP API":
                    params = {**test_case["params"], "api_key": key}
                    async with session.get(test_case["url"], params=params) as response:
                        result = await response.json()
                        return {"status": "working", "response": result}

                else:
                    async with session.get(test_case["url"], headers=headers) as response:
                        result = await response.json()
                        return {"status": "working", "response": result}

        except Exception as e:
            logger.error(f"Error testing {name}: {str(e)}")
            return {"status": "failed", "error": str(e)}

    async def run_quick_tests(self):
        """Run quick tests on all APIs in CSV"""
        # Read CSV
        df = pd.read_csv("apis.csv")
        
        results = {
            "working": [],
            "failed": [],
            "unknown": []
        }

        for _, row in df.iterrows():
            name = row.get("Name", "Unknown")
            key = row.get("API KEY")
            platform = row.get("Platform")

            if not key or not platform:
                results["unknown"].append({"name": name, "reason": "Missing key or platform"})
                continue

            logger.info(f"Testing {name} ({platform})")
            result = await self.test_api(name, key, platform)
            
            if result["status"] == "working":
                results["working"].append({
                    "name": name,
                    "platform": platform,
                    "key": key
                })
            elif result["status"] == "failed":
                results["failed"].append({
                    "name": name,
                    "platform": platform,
                    "error": result.get("error")
                })
            else:
                results["unknown"].append({
                    "name": name,
                    "platform": platform,
                    "reason": result.get("message")
                })

        # Generate results files
        self._save_results(results)
        return results

    def _save_results(self, results):
        """Save results to files"""
        # Save working APIs to .env.working
        with open(".env.working", "w") as f:
            f.write("# Working APIs\n\n")
            for api in results["working"]:
                f.write(f"{api['platform'].upper().replace(' ', '_')}_API_KEY={api['key']}\n")

        # Save failed APIs to .env.not-working
        with open(".env.not-working", "w") as f:
            f.write("# Failed APIs\n\n")
            for api in results["failed"]:
                f.write(f"# {api['platform'].upper().replace(' ', '_')}_API_KEY - Error: {api['error']}\n")

        # Save detailed report
        with open("logs/quick_test_report.md", "w") as f:
            f.write("# Quick API Test Report\n\n")
            
            f.write(f"## Working APIs ({len(results['working'])})\n")
            for api in results['working']:
                f.write(f"- {api['name']} ({api['platform']})\n")
            
            f.write(f"\n## Failed APIs ({len(results['failed'])})\n")
            for api in results['failed']:
                f.write(f"- {api['name']}: {api['error']}\n")
            
            f.write(f"\n## Unknown APIs ({len(results['unknown'])})\n")
            for api in results['unknown']:
                f.write(f"- {api['name']}: {api['reason']}\n")

async def main():
    tester = QuickAPITester()
    results = await tester.run_quick_tests()
    logger.info(f"Testing complete. Working APIs: {len(results['working'])}, Failed: {len(results['failed'])}, Unknown: {len(results['unknown'])}")

if __name__ == "__main__":
    asyncio.run(main()) 