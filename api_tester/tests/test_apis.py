import pytest
from api_validator import APIValidator
import asyncio
from loguru import logger
from pathlib import Path

@pytest.fixture
def api_validator():
    return APIValidator()

@pytest.mark.asyncio
async def test_all_apis(api_validator):
    """Test all APIs from CSV file"""
    # Get the absolute path to the CSV file
    csv_path = Path("../NOTIONDB/APIS 78466f7322194e6daf3528e0c09136a6_all.csv").resolve()
    
    if not csv_path.exists():
        logger.error(f"CSV file not found at {csv_path}")
        pytest.fail("CSV file not found")
    
    results = await api_validator.validate_all_apis(str(csv_path))
    
    # Generate test env file
    api_validator.generate_env_file(results, '.env.test')
    
    # Log results
    logger.info(f"Working APIs: {len(results['working'])}")
    logger.info(f"Failed APIs: {len(results['failed'])}")
    
    # Create detailed report
    report_path = Path("logs/api_test_report.md")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as report:
        report.write("# API Test Report\n\n")
        
        report.write("## Working APIs\n")
        for api in results['working']:
            report.write(f"- {api['name']}: Status {api['status']}\n")
            
        report.write("\n## Failed APIs\n")
        for api in results['failed']:
            report.write(f"- {api['name']}: {api['error']}\n")
    
    assert len(results['working']) > 0, "No working APIs found" 