import os
import sys
import pendulum
from pathlib import Path
from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from loguru import logger
import json
import shutil

class CrewAIAnalyzer:
    """Keeps our CrewAI implementation up-to-date with latest patterns"""
    
    def __init__(self):
        # Setup paths and system info
        self.root_dir = Path(__file__).parent.parent
        self.output_dir = self.root_dir / "crews/crew-output"
        self.backup_dir = self.root_dir / "crews/crew-backup"
        
        # Create necessary directories
        for directory in [self.output_dir, self.backup_dir]:
            directory.mkdir(exist_ok=True, parents=True)
        
        # Load environment
        load_dotenv(self.root_dir / '.env')
        
        # Setup logging
        logger.add(
            self.output_dir / "crewai_analyzer.log",
            rotation="1 day",
            retention="30 days",
            level="INFO"
        )
        
        # Initialize DuckDuckGo search
        self.search_tool = DuckDuckGoSearchRun()
        
        # System info for context
        self.system_info = self.get_system_info()
        
        # Initialize agents with system context
        self.initialize_agents()

    def get_system_info(self) -> Dict[str, Any]:
        """Gather system information for context"""
        return {
            "timestamp": pendulum.now().to_iso8601_string(),
            "python_version": sys.version,
            "platform": sys.platform,
            "working_directory": str(self.root_dir),
            "available_memory": self.get_memory_info(),
            "cpu_count": os.cpu_count()
        }

    def get_memory_info(self) -> str:
        """Get system memory information"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return f"{memory.available / (1024 * 1024 * 1024):.2f}GB available"
        except ImportError:
            return "Memory info unavailable"

    def initialize_agents(self):
        """Initialize agents with system context"""
        system_context = f"""Working in environment:
        - Timestamp: {self.system_info['timestamp']}
        - Python: {self.system_info['python_version']}
        - Platform: {self.system_info['platform']}
        - Directory: {self.system_info['working_directory']}
        """
        
        # Documentation Analyzer
        self.doc_analyzer = Agent(
            role='CrewAI Documentation Expert',
            goal='Monitor and analyze CrewAI documentation for latest patterns',
            backstory=f"""You are an expert at analyzing CrewAI documentation and 
            identifying best practices and new features. {system_context}""",
            tools=[self.search_tool],
            verbose=True
        )
        
        # Implementation Architect
        self.architect = Agent(
            role='Integration Architect',
            goal='Design optimal CrewAI implementation patterns',
            backstory=f"""You specialize in designing robust CrewAI implementations
            that follow best practices. {system_context}""",
            tools=[self.search_tool],
            verbose=True
        )
        
        # Code Generator
        self.generator = Agent(
            role='Code Generator',
            goal='Generate updated CrewAI implementation code',
            backstory=f"""You excel at generating clean, well-documented code that
            implements CrewAI best practices. {system_context}""",
            tools=[self.search_tool],
            verbose=True
        )

    def analyze_crewai_updates(self):
        """Analyze latest CrewAI patterns and update our implementation"""
        try:
            logger.info("Starting CrewAI analysis...")
            
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
                agent=self.doc_analyzer
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
                """,
                agent=self.generator
            )

            # Create and run crew
            crew = Crew(
                agents=[self.doc_analyzer, self.architect, self.generator],
                tasks=[research_task, architecture_task, documentation_task],
                verbose=True
            )

            result = crew.kickoff()
            
            # Save results
            output_dir = self.root_dir / 'crews/crew-output'
            output_dir.mkdir(exist_ok=True)
            
            with open(output_dir / 'crewai_analysis.md', 'w') as f:
                f.write(result)
                
            logger.success("CrewAI analysis complete")
            return result

        except Exception as e:
            logger.error(f"CrewAI analysis failed: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        analyzer = CrewAIAnalyzer()
        analyzer.analyze_crewai_updates()
    except Exception as e:
        logger.error(f"Failed to run CrewAI analyzer: {str(e)}") 