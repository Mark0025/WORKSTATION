import pytest
from pathlib import Path
from api_analyzer import APIAnalyzer
import asyncio
from loguru import logger

@pytest.fixture
def analyzer():
    return APIAnalyzer()

@pytest.mark.asyncio
async def test_api_analysis(analyzer):
    """Test API analysis with our CSV file"""
    # Use local path to CSV
    csv_path = Path("apis.csv").resolve()
    
    if not csv_path.exists():
        logger.error(f"CSV file not found at {csv_path}")
        pytest.fail("CSV file not found")
    
    results = await analyzer.analyze_apis_from_csv(str(csv_path))
    
    # Log summary
    logger.info(f"Analysis complete:")
    logger.info(f"Working APIs: {len(results['working_apis'])}")
    logger.info(f"Invalid APIs: {len(results['invalid_apis'])}")
    logger.info(f"Need Investigation: {len(results['needs_investigation'])}")
    
    # Basic assertions
    assert results is not None
    assert isinstance(results, dict)
    assert 'working_apis' in results 