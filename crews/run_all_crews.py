from pathlib import Path
from loguru import logger
import asyncio
from typing import List
import importlib
import inspect
from crews.base_crew import BaseCrew
from datetime import datetime

class CrewRunner:
    def __init__(self):
        self.output_dir = Path("crews/crew-output/runs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logger.add(
            self.output_dir / "crew_runner_{time}.log",
            rotation="500 MB",
            level="INFO"
        )

    async def run_crew_with_delay(self, crew: BaseCrew, delay: int = 30):
        """Run a single crew with delay and monitoring"""
        try:
            start_time = datetime.now()
            crew_name = crew.__class__.__name__
            
            logger.info(f"Starting {crew_name} at {start_time}")
            
            # Run the crew
            result = await crew.run()
            
            # Calculate runtime
            end_time = datetime.now()
            runtime = end_time - start_time
            
            # Log completion
            logger.success(f"""
                Crew: {crew_name}
                Runtime: {runtime}
                Completed at: {end_time}
            """)
            
            # Add delay before next crew
            logger.info(f"Waiting {delay} seconds before next crew...")
            await asyncio.sleep(delay)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to run {crew.__class__.__name__}: {str(e)}")
            raise

    async def run_all_crews(self, delay_between_crews: int = 30):
        """Run all crews with delay between each"""
        try:
            # Get all crew files
            crews_dir = Path(__file__).parent
            crew_files = crews_dir.glob("*_crew.py")
            
            # Load all crew classes
            crews = []
            for file in crew_files:
                if file.stem == "base_crew":
                    continue
                    
                # Import the module using absolute import
                module_name = f"crews.{file.stem}"
                module = importlib.import_module(module_name)
                
                # Find crew class in module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseCrew) and 
                        obj != BaseCrew):
                        crews.append(obj())
                        break
            
            logger.info(f"Found {len(crews)} crews to run")
            
            # Run each crew with delay
            for i, crew in enumerate(crews, 1):
                logger.info(f"Running crew {i} of {len(crews)}: {crew.__class__.__name__}")
                await self.run_crew_with_delay(crew, delay_between_crews)
            
            logger.success("All crews completed")
            
        except Exception as e:
            logger.error(f"Failed to run crews: {str(e)}")
            raise

if __name__ == "__main__":
    runner = CrewRunner()
    # Run with 30 second delay between crews
    asyncio.run(runner.run_all_crews(delay_between_crews=30)) 