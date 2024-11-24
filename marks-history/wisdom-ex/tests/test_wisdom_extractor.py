import pytest
from pathlib import Path
import sys
import json

# Add the wisdom-ex directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from app import WisdomExtractor

def test_wisdom_extractor_initialization():
    extractor = WisdomExtractor()
    assert extractor.base_dir.exists()
    assert extractor.index_file.exists()
    
    # Check if index.json has correct initial structure
    with open(extractor.index_file) as f:
        index = json.load(f)
        assert "projects" in index
        assert isinstance(index["projects"], list)

def test_sanitize_filename():
    extractor = WisdomExtractor()
    test_title = "This is a Test! Video (2024) @author"
    sanitized = extractor.sanitize_filename(test_title)
    assert " " not in sanitized
    assert "!" not in sanitized
    assert "(" not in sanitized
    assert "@" not in sanitized

def test_extract_links():
    extractor = WisdomExtractor()
    test_text = """
    Check out https://github.com/user/repo1 and
    https://github.com/user/repo2
    Also visit https://example.com and
    https://test.com
    """
    links = extractor.extract_links(test_text)
    assert len(links["github_repos"]) == 2
    assert len(links["other_links"]) == 2
    assert "https://github.com/user/repo1" in links["github_repos"]
    assert "https://example.com" in links["other_links"] 