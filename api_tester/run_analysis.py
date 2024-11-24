import asyncio
from loguru import logger
import sys
from pathlib import Path

# Set up logging
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")
logger.add("logs/analysis.log", rotation="100 MB")

async def run_full_analysis():
    try:
        # 1. Run quick test report
        logger.info("Generating quick test report...")
        from quick_test_report import generate_quick_report
        await generate_quick_report()
        logger.success("Quick test report generated")

        # 2. Create visualization
        logger.info("Creating API visualization...")
        from visualize_apis import create_api_visualization
        create_api_visualization()
        logger.success("API visualization created")

        # 3. Monitor API health
        logger.info("Checking API health...")
        from monitor_apis import APIMonitor
        monitor = APIMonitor()
        await monitor.monitor_all_apis()
        logger.success("API health check completed")

        logger.info("Analysis complete! Check the following files:")
        logger.info("- logs/quick_test_report.md")
        logger.info("- api_ecosystem.png")
        logger.info("- logs/api_health_report.md")
        logger.info("- logs/analysis.log")

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    
    # Run the analysis
    asyncio.run(run_full_analysis()) 