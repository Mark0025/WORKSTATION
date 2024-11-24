from pathlib import Path
import importlib
from loguru import logger

def verify_packages():
    """Verify both package installations"""
    results = {
        'workstation': False,
        'timeline': False,
        'timeline_in_workstation': False
    }
    
    try:
        # Try standalone timeline
        import timeline
        results['timeline'] = True
        logger.success("✅ Timeline package (standalone) verified")
    except ImportError as e:
        logger.error(f"❌ Timeline package import failed: {e}")
    
    try:
        # Try workstation
        import workstation
        results['workstation'] = True
        logger.success("✅ Workstation package verified")
    except ImportError as e:
        logger.error(f"❌ Workstation package import failed: {e}")
        
    try:
        # Try timeline in workstation
        from workstation.timeline import TimelineWatcher
        results['timeline_in_workstation'] = True
        logger.success("✅ Timeline in workstation verified")
    except ImportError as e:
        logger.error(f"❌ Timeline in workstation import failed: {e}")
        
    return results

if __name__ == "__main__":
    results = verify_packages()
    
    if all(results.values()):
        logger.success("All packages verified successfully!")
    else:
        logger.warning("Some package verifications failed")
        for pkg, status in results.items():
            logger.info(f"{pkg}: {'✅' if status else '❌'}") 