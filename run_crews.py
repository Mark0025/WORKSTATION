from crews.run_all_crews import CrewRunner
import asyncio

if __name__ == "__main__":
    runner = CrewRunner()
    asyncio.run(runner.run_all_crews(delay_between_crews=30)) 