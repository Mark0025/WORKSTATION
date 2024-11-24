import os
from pathlib import Path
from crewai import Agent, Task, Crew
from langchain.tools import BaseTool, StructuredTool, Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SerpAPIWrapper
from typing import Optional
from dotenv import load_dotenv
from loguru import logger

# Load environment
root_dir = Path(__file__).parent.parent
load_dotenv(root_dir / '.env')

class DockerAnalyzer:
    """Analyzes Docker services using our working APIs"""
    
    def __init__(self):
        # Initialize tools properly
        self.search = DuckDuckGoSearchRun()
        
        # Define tools using proper structure
        self.tools = [
            Tool(
                name="Web Search",
                func=self.search.run,
                description="""Use this tool to search for Docker documentation, 
                best practices, and configuration examples."""
            )
        ]
        
        # Expert agent with proper tool configuration
        self.docker_expert = Agent(
            role='Docker Expert',
            goal='Analyze Docker services and provide best practices',
            backstory="""You are a Docker expert who analyzes container setups 
            and provides detailed configuration advice.""",
            tools=self.tools,
            verbose=True,
            allow_delegation=True  # New feature in latest CrewAI
        )

        # Integration specialist
        self.integration_specialist = Agent(
            role='Integration Architect',
            goal='Design secure and efficient Docker service integrations',
            backstory="""You specialize in creating robust Docker service 
            architectures with security and performance in mind.""",
            tools=self.tools,
            verbose=True,
            allow_delegation=True
        )

    def analyze_setup(self):
        """Analyze our Docker setup"""
        try:
            logger.info("Starting Docker analysis...")
            
            # Research task with context
            research_task = Task(
                description="""
                Analyze our Docker services:
                - nginx
                - postgres
                - redis
                - mongodb
                - rabbitmq
                - elasticsearch
                - portainer
                
                For each:
                1. Check configuration best practices
                2. Identify security considerations
                3. Note resource requirements
                4. List common issues
                """,
                agent=self.docker_expert,
                context="""We are running these services in production and need
                detailed analysis of security and performance configurations."""
            )

            # Integration task with context
            integration_task = Task(
                description="""
                Based on the research:
                1. Map service connections
                2. Document data flows
                3. Note security patterns
                4. List optimization opportunities
                """,
                agent=self.integration_specialist,
                context="""Focus on secure communication between services and 
                efficient resource usage patterns."""
            )

            # Create crew with new features
            crew = Crew(
                agents=[self.docker_expert, self.integration_specialist],
                tasks=[research_task, integration_task],
                verbose=True,
                process="sequential",  # New way to specify process
                manager_llm="gpt-4"  # Optional: specify manager LLM
            )

            # Better result handling
            try:
                result = crew.kickoff()
                
                # Save results with proper path handling
                output_dir = Path("crews/crew-output")
                output_dir.mkdir(exist_ok=True, parents=True)
                
                output_file = output_dir / "docker_analysis.md"
                output_file.write_text(result)
                
                logger.success(f"Analysis saved to {output_file}")
                return result
                
            except Exception as e:
                logger.error(f"Crew execution failed: {str(e)}")
                raise

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        analyzer = DockerAnalyzer()
        analyzer.analyze_setup()
    except Exception as e:
        logger.error(f"Failed to run analysis: {str(e)}") 