from src.utils.file_utils import sanitize_filename, ensure_directory
from pathlib import Path

def test_sanitize_filename():
    test_title = "This is a Test! Video (2024) @author"
    sanitized = sanitize_filename(test_title)
    assert " " not in sanitized
    assert "!" not in sanitized
    assert "(" not in sanitized
    assert "@" not in sanitized

def test_ensure_directory():
    test_dir = Path("test_dir")
    created_dir = ensure_directory(test_dir)
    assert created_dir.exists()
    assert created_dir.is_dir()
    test_dir.rmdir()  # Cleanup 