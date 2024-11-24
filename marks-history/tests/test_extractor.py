import pytest
from pathlib import Path
from src.extractor import WisdomExtractor

def test_wisdom_extractor_initialization():
    extractor = WisdomExtractor()
    assert extractor.base_dir.exists()
    assert extractor.index_file.exists()

def test_get_video_info():
    extractor = WisdomExtractor()
    title, author = extractor.get_video_info("https://www.youtube.com/watch?v=test")
    assert isinstance(title, str)
    assert isinstance(author, str) 