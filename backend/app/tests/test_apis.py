import pytest
from app.tests.api_validator import APIValidator
import asyncio
from loguru import logger

@pytest.fixture
def api_validator():
    return APIValidator()

@pytest.mark.asyncio
async def test_all_apis(api_validator):
    """Test all APIs from CSV file"""
    csv_path = "NOTIONDB/APIS 78466f7322194e6daf3528e0c09136a6_all.csv"
    results = await api_validator.validate_all_apis(csv_path)
    
    # Generate test env file
    api_validator.generate_env_file(results, '.env.test')
    
    # Log results
    logger.info(f"Working APIs: {len(results['working'])}")
    logger.info(f"Failed APIs: {len(results['failed'])}")
    
    # Create detailed report
    with open('logs/api_test_report.md', 'w') as report:
        report.write("# API Test Report\n\n")
        
        report.write("## Working APIs\n")
        for api in results['working']:
            report.write(f"- {api['name']}: Status {api['status']}\n")
            
        report.write("\n## Failed APIs\n")
        for api in results['failed']:
            report.write(f"- {api['name']}: {api['error']}\n")
    
    assert len(results['working']) > 0, "No working APIs found" 