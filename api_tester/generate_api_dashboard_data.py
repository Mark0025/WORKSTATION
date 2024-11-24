import json
from pathlib import Path
import pandas as pd
from loguru import logger
import pendulum
from typing import Dict, Any
from config.naming_standards import APINameStandards

class APIDashboardGenerator:
    def __init__(self):
        self.visualization_dir = Path("visualization")
        self.visualization_dir.mkdir(exist_ok=True)
        self.logger = logger
        self.logger.add("logs/dashboard_generator.log", 
                       format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
        
        # Initialize timezone
        self.timezone = pendulum.timezone('America/Chicago')
        
        # API Categories with standardized names
        self.api_categories = {
            "Open_AI": "ai_services",
            "GO_HIGH_LEVEL": "marketing",
            "SERP_API": "search",
            "GitHub": "development",
            "Mail_Gun": "communication",
            "Zapier": "automation",
            "Slack": "communication",
            "Zoom": "communication",
            "Docker": "development",
            "Twilio": "communication",
            "DeepGram": "ai_services",
            "Weaviate": "ai_services",
            "Hugging_Face": "ai_services",
            "Claude": "ai_services",
            "Google_Search": "search",
            "Super_AGI": "ai_services",
            "LangChain": "ai_services",
            "AutoGen": "ai_services",
            "JIRA": "development",
            "Notion": "productivity"
        }

        self.name_standards = APINameStandards()

    def _get_last_check_time(self) -> str:
        """Get formatted timestamp in local timezone"""
        return pendulum.now(self.timezone).format('YYYY-MM-DD HH:mm:ss')

    def _get_status_details(self, row) -> Dict[str, Any]:
        """Get detailed status information with proper timestamps"""
        now = pendulum.now(self.timezone)
        
        return {
            "last_checked": now.format('YYYY-MM-DD HH:mm:ss'),
            "next_check": now.add(hours=1).format('YYYY-MM-DD HH:mm:ss'),
            "status_message": self._get_status_message(row),
            "is_billing_active": self._check_billing_status(row),
            "uptime_last_24h": self._get_uptime_last_24h(row)
        }

    def _get_uptime_last_24h(self, row) -> Dict[str, Any]:
        """Calculate uptime for last 24 hours"""
        now = pendulum.now(self.timezone)
        yesterday = now.subtract(days=1)
        
        return {
            "start_time": yesterday.format('YYYY-MM-DD HH:mm:ss'),
            "end_time": now.format('YYYY-MM-DD HH:mm:ss'),
            "uptime_percentage": self._calculate_uptime(row, yesterday, now)
        }

    def _calculate_uptime(self, row, start: pendulum.DateTime, end: pendulum.DateTime) -> float:
        """Calculate uptime percentage between two timestamps"""
        try:
            with open("logs/quick_test.log", "r") as f:
                log_content = f.read()
                # Simple calculation - can be made more sophisticated
                if row["Name"] in log_content and "working" in log_content:
                    return 100.0
                elif row["Name"] in log_content and "failed" in log_content:
                    return 0.0
                return 50.0  # Unknown status
        except FileNotFoundError:
            return 0.0

    def _save_dashboard_data(self, data: Dict[str, Any]):
        """Save dashboard data with timestamp"""
        output_data = {
            "generated_at": pendulum.now(self.timezone).format('YYYY-MM-DD HH:mm:ss'),
            "data": data
        }
        
        output_file = self.visualization_dir / "api_dashboard_data.json"
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2)
        
        self.logger.info(f"Dashboard data saved to {output_file}")

    def generate_dashboard_data(self):
        """Generate data for API ecosystem dashboard"""
        try:
            start_time = pendulum.now(self.timezone)
            self.logger.info(f"Starting dashboard generation at {start_time.format('YYYY-MM-DD HH:mm:ss')}")
            
            # Initialize categories
            api_data = {
                "ai_services": {
                    "name": "AI & Machine Learning",
                    "apis": [],
                    "total_active": 0,
                    "last_updated": start_time.format('YYYY-MM-DD HH:mm:ss')
                },
                "marketing": {
                    "name": "Marketing & CRM",
                    "apis": [],
                    "total_active": 0,
                    "last_updated": start_time.format('YYYY-MM-DD HH:mm:ss')
                },
                # ... (other categories)
            }
            
            # Process APIs
            df = pd.read_csv("apis.csv")
            for _, row in df.iterrows():
                category = self.api_categories.get(row["Platform"], "other")
                api_info = self._process_api_info(row)
                api_data[category]["apis"].append(api_info)
                
                if api_info["status"] == "active":
                    api_data[category]["total_active"] += 1
            
            # Add generation metadata
            end_time = pendulum.now(self.timezone)
            api_data["metadata"] = {
                "generation_started": start_time.format('YYYY-MM-DD HH:mm:ss'),
                "generation_completed": end_time.format('YYYY-MM-DD HH:mm:ss'),
                "duration_seconds": end_time.diff(start_time).in_seconds()
            }
            
            self._save_dashboard_data(api_data)
            self.logger.success(f"Dashboard generation completed in {end_time.diff(start_time).in_seconds()} seconds")
            
        except Exception as e:
            self.logger.error(f"Error generating dashboard data: {str(e)}")
            raise

    def _process_api_info(self, row) -> Dict[str, Any]:
        """Process individual API information"""
        now = pendulum.now(self.timezone)
        return {
            "name": row["Name"],
            "platform": row["Platform"],
            "status": self._check_api_status(row),
            "last_checked": now.format('YYYY-MM-DD HH:mm:ss'),
            "next_check": now.add(hours=1).format('YYYY-MM-DD HH:mm:ss'),
            "details": self._get_api_details(row)
        }

    def _check_api_status(self, row) -> str:
        """Check API status from logs and determine current state"""
        try:
            with open("logs/quick_test.log", "r") as f:
                log_content = f.read()
                api_name = row["Name"]
                
                # Standardize API names based on linter suggestions
                api_name = self._standardize_api_name(api_name)
                
                if api_name in log_content:
                    if "working" in log_content:
                        return "active"
                    elif "billing_not_active" in log_content:
                        return "billing_required"
                    elif "failed" in log_content:
                        return "failed"
                return "unknown"
        except FileNotFoundError:
            self.logger.warning(f"Log file not found for API status check: {row['Name']}")
            return "unknown"

    def _standardize_api_name(self, name: str) -> str:
        """Standardize API name using naming standards"""
        return self.name_standards.standardize_name(name)

    def _get_api_category(self, name: str) -> str:
        """Get API category using naming standards"""
        return self.name_standards.get_category(name)

if __name__ == "__main__":
    generator = APIDashboardGenerator()
    generator.generate_dashboard_data() 