from pathlib import Path
import sys
from loguru import logger

def verify_package_structure():
    """Verify Python package structure and imports"""
    logger.info("Verifying package structure...")
    
    issues = []
    required_dirs = ["timeline", "crews", "scripts"]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        
        # Check directory exists
        if not dir_path.exists():
            issues.append(f"❌ Directory {dir_name} missing")
            continue
            
        # Check __init__.py exists
        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            issues.append(f"❌ Missing __init__.py in {dir_name}")
            
        # Check subdirectories
        for subdir in dir_path.glob("**/"):
            if subdir.is_dir() and subdir != dir_path:
                sub_init = subdir / "__init__.py"
                if not sub_init.exists():
                    issues.append(f"❌ Missing __init__.py in {subdir}")
                    
    if issues:
        logger.warning("Found package structure issues:")
        for issue in issues:
            logger.warning(issue)
        return False
    
    logger.success("Package structure verified!")
    return True

if __name__ == "__main__":
    if not verify_package_structure():
        sys.exit(1) 