import json
from pathlib import Path
import pandas as pd
from loguru import logger

class VisualizationDataGenerator:
    def __init__(self):
        self.visualization_dir = Path("visualization")
        self.visualization_dir.mkdir(exist_ok=True)

    def generate_data(self):
        """Generate data for visualization"""
        try:
            # Read API status from our test results
            df = pd.read_csv("apis.csv")
            
            # Group APIs by category
            api_data = {
                "ai_services": [],
                "marketing": [],
                "search": [],
                "development": []
            }
            
            # Process each API
            for _, row in df.iterrows():
                category = self._determine_category(row["Platform"])
                if category:
                    api_data[category].append({
                        "name": row["Name"],
                        "status": self._check_api_status(row),
                        "platform": row["Platform"]
                    })
            
            # Save data for visualization
            with open(self.visualization_dir / "api_data.json", "w") as f:
                json.dump(api_data, f, indent=2)
                
            logger.info("Visualization data generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating visualization data: {str(e)}")
            raise

    def _determine_category(self, platform: str) -> str:
        """Determine API category based on platform"""
        categories = {
            "Open_AI": "ai_services",
            "GO HIGH LEVEL": "marketing",
            "SERP API": "search",
            "Github": "development"
        }
        return categories.get(platform, "other")

    def _check_api_status(self, api_data) -> str:
        """Check API status based on our tests"""
        # Implementation would check against our test results
        return "active"  # Placeholder

if __name__ == "__main__":
    generator = VisualizationDataGenerator()
    generator.generate_data() 