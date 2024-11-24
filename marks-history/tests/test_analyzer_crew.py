import pytest
from pathlib import Path
import sys

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from wisdom_ex.analyzer_crew import WisdomAnalyzerCrew
from loguru import logger

def test_analyzer_crew_logging(tmp_path):
    # Setup test log file
    log_file = tmp_path / "test.log"
    logger.add(log_file, format="{message}")
    
    # Create test wisdom directory
    wisdom_dir = tmp_path / "test-wisdom"
    wisdom_dir.mkdir()
    (wisdom_dir / "wisdom.md").write_text("## TEST\n- Test content")
    (wisdom_dir / "metadata.json").write_text('{"title": "unknown"}')
    
    # Run analyzer
    crew = WisdomAnalyzerCrew(str(wisdom_dir))
    try:
        crew.analyze_wisdom()
    except Exception:
        pass  # We're testing logging, not functionality
    
    # Check logs
    logs = log_file.read_text()
    assert "Starting wisdom analysis" in logs
    assert "Initializing WisdomAnalyzerCrew" in logs 