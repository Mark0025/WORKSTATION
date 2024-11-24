from pathlib import Path
from loguru import logger
from datetime import datetime
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
import os
from typing import List

class BaseCrew:
    """Base class for all crews with common functionality"""
    
    def __init__(self, output_dir: str):
        # Setup paths
        self.output_dir = Path(f"crews/crew-output/{output_dir}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        log_path = Path("crews/crew-output/logs")
        log_path.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_path / f"{output_dir}_{{time}}.log",
            rotation="500 MB",
            level="INFO"
        )
        
        # Initialize OpenAI (using 3.5 for testing)
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Initialize tools
        self.search = DuckDuckGoSearchRun()
        self.tools = [
            Tool(
                name="Search",
                func=self.search.run,
                description="Search for information"
            )
        ]
        
        # Add ecosystem visualization agent
        self.ecosystem_visualizer = Agent(
            role='Ecosystem Visualizer',
            goal='Create system relationship diagrams',
            backstory="""You create clear Mermaid diagrams showing how 
            different systems and APIs interact.""",
            llm=self.llm,
            tools=self.tools,
            verbose=True
        )
        
        logger.info(f"Initialized {self.__class__.__name__}")

    def save_output(self, content: str, filename: str) -> Path:
        """Save output with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"{filename}_{timestamp}.md"
        output_file.write_text(content)
        logger.info(f"Saved output to {output_file}")
        return output_file

    def create_mermaid_diagram(self, data: str, filename: str) -> Path:
        """Create and save a Mermaid diagram"""
        diagram = f"""
```mermaid
{data}
```
"""
        return self.save_output(diagram, f"{filename}_diagram")

    def create_ecosystem_diagram(self, components: List[str]) -> str:
        """Create a Mermaid diagram showing system relationships"""
        try:
            # Create visualization task
            task = Task(
                description=f"""
                Create a Mermaid diagram showing relationships between:
                {', '.join(components)}
                
                Include:
                1. API connections
                2. Data flows
                3. Integration points
                4. Dependencies
                
                Use proper Mermaid syntax.
                """,
                agent=self.ecosystem_visualizer
            )
            
            # Run task
            crew = Crew(
                agents=[self.ecosystem_visualizer],
                tasks=[task],
                verbose=True
            )
            
            result = crew.kickoff()
            
            # Save diagram
            self.create_mermaid_diagram(result, "ecosystem")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to create ecosystem diagram: {str(e)}")
            raise

    def run(self):
        """Must be implemented by child classes"""
        raise NotImplementedError 