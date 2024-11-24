from crews.base_crew import BaseCrew
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import TimelineEvent
from datetime import datetime, timedelta
import os

class TimelineAnalyzerCrew(BaseCrew):
    def __init__(self):
        super().__init__("timeline-analysis")
        
        # Initialize OpenAI with the working key
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
                description="Search for development patterns and best practices"
            )
        ]
        
        # Create Pattern Analyzer
        self.pattern_analyzer = Agent(
            role='Pattern Analyzer',
            goal='Analyze development patterns and suggest improvements',
            backstory="""You analyze development patterns and identify areas 
            for improvement in development workflows.""",
            llm=self.llm,
            tools=self.tools,
            verbose=True
        )
        
        # Create Code Reviewer
        self.code_reviewer = Agent(
            role='Code Reviewer',
            goal='Review code changes and suggest improvements',
            backstory="""You review code changes and provide constructive feedback
            for better code quality and architecture.""",
            llm=self.llm,
            tools=self.tools,
            verbose=True
        )
        
        # Create Documentation Expert
        self.doc_expert = Agent(
            role='Documentation Expert',
            goal='Create clear documentation from analysis',
            backstory="""You create clear, actionable documentation from 
            analysis findings.""",
            llm=self.llm,
            tools=self.tools,
            verbose=True
        )
        
        logger.info(f"Initialized {self.__class__.__name__}")

    def analyze_timeline(self, days_back=7):
        """Analyze recent timeline events"""
        try:
            # Get recent events
            since_date = datetime.now() - timedelta(days=days_back)
            
            # Create analysis task
            analysis_task = Task(
                description=f"""
                Analyze the development timeline since {since_date.strftime('%Y-%m-%d')}:
                
                1. Identify patterns in:
                   - Code changes
                   - AI interactions
                   - Development workflow
                
                2. Look for:
                   - Common challenges
                   - Repeated questions
                   - Workflow bottlenecks
                   
                3. Suggest improvements for:
                   - Code quality
                   - Development speed
                   - AI utilization
                """,
                agent=self.pattern_analyzer
            )
            
            # Create review task
            review_task = Task(
                description="""
                Review the code changes and AI interactions:
                
                1. Evaluate code quality
                2. Check for consistent patterns
                3. Identify areas for improvement
                4. Suggest better practices
                """,
                agent=self.code_reviewer
            )
            
            # Create documentation task
            doc_task = Task(
                description="""
                Create clear documentation from the analysis:
                
                1. Summarize findings
                2. List actionable improvements
                3. Provide specific examples
                4. Create improvement roadmap
                """,
                agent=self.doc_expert
            )
            
            # Run crew
            crew = Crew(
                agents=[self.pattern_analyzer, self.code_reviewer, self.doc_expert],
                tasks=[analysis_task, review_task, doc_task],
                verbose=True
            )
            
            result = crew.kickoff()
            
            # Save analysis with timestamp
            self.save_output(result, f"timeline_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise