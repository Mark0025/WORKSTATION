import pytest
import json
from pathlib import Path
from app.core.logger import setup_logger

@pytest.fixture
def logger():
    return setup_logger("test_logger")

def test_logger_creates_files(logger):
    """Test that log files are created"""
    log_dir = Path("logs")
    assert log_dir.exists()
    assert (log_dir / "app.log").exists()
    assert (log_dir / "error.log").exists()

def test_logger_json_format(logger):
    """Test that logs are properly formatted in JSON"""
    test_message = "Test log message"
    logger.info(test_message)
    
    with open("logs/app.log", "r") as f:
        last_log = f.readlines()[-1]
        log_data = json.loads(last_log)
        
        assert log_data["message"] == test_message
        assert "timestamp" in log_data
        assert "level" in log_data
        assert "module" in log_data

def test_error_logging(logger):
    """Test that errors are properly logged"""
    try:
        raise ValueError("Test error")
    except ValueError as e:
        logger.error("Error occurred", exc_info=True)
        
    with open("logs/error.log", "r") as f:
        last_log = f.readlines()[-1]
        log_data = json.loads(last_log)
        
        assert "Test error" in log_data["exception"]
        assert log_data["level"] == "ERROR" 