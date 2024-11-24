from config.naming_standards import APINameStandards
from loguru import logger
import pandas as pd

def test_api_names():
    """Test API names from CSV against standards"""
    try:
        # Read CSV file
        df = pd.read_csv("apis.csv")
        
        # Test each API name
        corrections = []
        for _, row in df.iterrows():
            name = row["Name"]
            is_valid, standard_name = APINameStandards.validate_name(name)
            
            if not is_valid:
                corrections.append({
                    "original": name,
                    "suggested": standard_name
                })
        
        # Log results
        logger.info(f"Found {len(corrections)} names needing standardization")
        for correction in corrections:
            logger.info(f"Suggest changing '{correction['original']}' to '{correction['suggested']}'")
            
    except Exception as e:
        logger.error(f"Error testing API names: {str(e)}")

if __name__ == "__main__":
    logger.add("logs/naming_test.log")
    test_api_names() 