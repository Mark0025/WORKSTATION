import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
from loguru import logger

# Load environment
root_dir = Path(__file__).parent.parent
load_dotenv(root_dir / '.env')

class CrewAIDocumenter:
    """Documents CrewAI capabilities and integrates with our ecosystem"""
    
    def __init__(self):
        # Initialize search tools
        self.search = DuckDuckGoSearchRun()
        self.serp = SerpAPIWrapper()
        
        # Documentation researcher
        self.researcher = Agent(
            role='CrewAI Documentation Researcher',
            goal='Research and analyze CrewAI documentation comprehensively',
            backstory="""You are an expert at analyzing documentation and 
            understanding framework capabilities.""",
            tools=[
                Tool(
                    name="Search",
                    func=self.search.run,
                    description="Search for CrewAI documentation"
                ),
                Tool(
                    name="Deep Search",
                    func=self.serp.run,
                    description="Detailed search of CrewAI capabilities"
                )
            ],
            verbose=True
        )

        # Integration architect
        self.architect = Agent(
            role='Integration Architect',
            goal='Design integration patterns between CrewAI and our ecosystem',
            backstory="""You design how CrewAI capabilities can be integrated
            into existing systems.""",
            tools=[
                Tool(
                    name="Search",
                    func=self.search.run,
                    description="Research integration patterns"
                )
            ],
            verbose=True
        )

        # Documentation writer
        self.writer = Agent(
            role='Technical Documentation Writer',
            goal='Create clear, actionable documentation and diagrams',
            backstory="""You excel at creating technical documentation and
            visual representations of systems.""",
            tools=[
                Tool(
                    name="Search",
                    func=self.search.run,
                    description="Research documentation best practices"
                )
            ],
            verbose=True
        )

    def document_crewai(self):
        """Analyze and document CrewAI capabilities"""
        try:
            # Research task
            research_task = Task(
                description="""
                Research CrewAI documentation at https://docs.crewai.com/:
                1. Core concepts and capabilities
                2. Available tools and integrations
                3. Best practices and patterns
                4. Custom tool creation
                5. Integration approaches
                
                Focus on how these can be used in our ecosystem.
                """,
                agent=self.researcher
            )

            # Architecture task
            architecture_task = Task(
                description="""
                Based on the research:
                1. Design integration patterns
                2. Map tool capabilities
                3. Identify automation opportunities
                4. Create integration diagrams
                
                Create a mermaid diagram showing how CrewAI integrates
                with our existing API ecosystem.
                """,
                agent=self.architect
            )

            # Documentation task
            documentation_task = Task(
                description="""
                Create comprehensive documentation including:
                1. Best practices guide
                2. Tool usage patterns
                3. Integration examples
                4. Visual diagrams
                
                Format in markdown with mermaid diagrams.
                Save in crews/crew-output/crewai_documentation.md
                """,
                agent=self.writer
            )

            # Create and run crew
            crew = Crew(
                agents=[self.researcher, self.architect, self.writer],
                tasks=[research_task, architecture_task, documentation_task],
                process=Process.sequential,
                verbose=True
            )

            result = crew.kickoff()
            
            # Ensure output directory exists
            output_dir = root_dir / 'crews/crew-output'
            output_dir.mkdir(exist_ok=True)
            
            # Save documentation
            with open(output_dir / 'crewai_documentation.md', 'w') as f:
                f.write(result)
                
            logger.success("CrewAI documentation generated")
            return result

        except Exception as e:
            logger.error(f"Documentation failed: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        documenter = CrewAIDocumenter()
        documenter.document_crewai()
    except Exception as e:
        logger.error(f"Failed to run documenter: {str(e)}") 