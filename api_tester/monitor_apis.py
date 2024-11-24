from loguru import logger
import asyncio
import aiohttp
from datetime import datetime
import json

class APIMonitor:
    def __init__(self):
        self.status = {}
        logger.add("logs/api_monitor.log")
    
    async def check_api_health(self, name: str, endpoint: str, headers: dict):
        """Check health of a single API"""
        try:
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                async with session.get(endpoint, headers=headers) as response:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    
                    return {
                        "name": name,
                        "status": response.status,
                        "response_time": elapsed,
                        "healthy": 200 <= response.status < 300
                    }
        except Exception as e:
            logger.error(f"Error checking {name}: {str(e)}")
            return {
                "name": name,
                "status": 500,
                "error": str(e),
                "healthy": False
            }

    async def monitor_all_apis(self):
        """Monitor all APIs and generate report"""
        # Load API configurations
        with open("api_config.json") as f:
            apis = json.load(f)
        
        results = []
        for api in apis:
            result = await self.check_api_health(
                api["name"],
                api["health_endpoint"],
                api["headers"]
            )
            results.append(result)
        
        # Generate monitoring report
        self._generate_report(results)
        
    def _generate_report(self, results):
        """Generate monitoring report"""
        with open("logs/api_health_report.md", "w") as f:
            f.write("# API Health Report\n\n")
            f.write(f"Generated at: {datetime.now()}\n\n")
            
            # Healthy APIs
            f.write("## Healthy APIs\n")
            healthy = [r for r in results if r["healthy"]]
            for api in healthy:
                f.write(f"- {api['name']}: {api['response_time']:.2f}s\n")
            
            # Unhealthy APIs
            f.write("\n## Unhealthy APIs\n")
            unhealthy = [r for r in results if not r["healthy"]]
            for api in unhealthy:
                f.write(f"- {api['name']}: {api.get('error', 'Unknown error')}\n")

if __name__ == "__main__":
    monitor = APIMonitor()
    asyncio.run(monitor.monitor_all_apis()) 