from config.naming_standards import APINameStandards
import pandas as pd
from loguru import logger

def validate_api_names(csv_path: str):
    """Validate API names in CSV against standards"""
    df = pd.read_csv(csv_path)
    
    validation_results = {
        "valid": [],
        "invalid": [],
        "suggestions": {}
    }
    
    for _, row in df.iterrows():
        name = row["Name"]
        if APINameStandards.is_valid_name(name):
            validation_results["valid"].append(name)
        else:
            validation_results["invalid"].append(name)
            # Get standardized suggestion
            suggestion = APINameStandards.standardize_name(name)
            if suggestion != name:
                validation_results["suggestions"][name] = suggestion
    
    return validation_results

if __name__ == "__main__":
    results = validate_api_names("apis.csv")
    
    logger.info(f"Valid API names: {len(results['valid'])}")
    logger.info(f"Invalid API names: {len(results['invalid'])}")
    
    if results["suggestions"]:
        logger.info("Suggested corrections:")
        for original, suggestion in results["suggestions"].items():
            logger.info(f"  {original} -> {suggestion}") 