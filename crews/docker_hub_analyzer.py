from crews.base_crew import BaseCrew
from crewai import Agent, Task, Crew
from loguru import logger

class DockerHubAnalyzer(BaseCrew):
    def __init__(self):
        super().__init__("docker-analysis")
        
        # Create Research Agent
        self.researcher = Agent(
            role='Docker Researcher',
            goal='Research Docker images and create visual diagrams',
            backstory="""You are a technical researcher who creates clear
            documentation with visual diagrams.""",
            llm=self.llm,
            tools=self.tools,
            verbose=True
        )

        # Create Visualization Expert
        self.visualizer = Agent(
            role='Visualization Expert',
            goal='Create clear diagrams of Docker architectures',
            backstory="""You excel at creating Mermaid diagrams to visualize
            technical architectures.""",
            llm=self.llm,
            tools=self.tools,
            verbose=True
        )

    def run(self):
        """Run the analysis with visualization"""
        try:
            # Research task
            research_task = Task(
                description="""
                Research these Docker images and create a diagram:
                - nginx
                - postgres
                - redis
                - mongodb
                
                For each image:
                1. Main use cases
                2. Common configurations
                3. Integration patterns
                
                Create a Mermaid diagram showing the relationships.
                """,
                agent=self.researcher
            )

            # Visualization task
            viz_task = Task(
                description="""
                Create a Mermaid diagram showing:
                1. Service relationships
                2. Data flows
                3. Network connections
                4. Volume mounts
                
                Use the research findings to create clear visualizations.
                """,
                agent=self.visualizer
            )

            # Create and run crew
            crew = Crew(
                agents=[self.researcher, self.visualizer],
                tasks=[research_task, viz_task],
                verbose=True
            )

            result = crew.kickoff()
            
            # Save results
            self.save_output(result, "docker_analysis")
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise 