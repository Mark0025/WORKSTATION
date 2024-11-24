from crewai import Agent, Task, Crew
from email_analyzer.database import SessionLocal, Email
from typing import List

class EmailAnalyst:
    def __init__(self):
        self.session = SessionLocal()

    def analyze_emails(self, limit: int = 10) -> List[dict]:
        # Get unanalyzed emails
        emails = self.session.query(Email).filter_by(analyzed=False).limit(limit).all()
        
        # Create CrewAI agents
        researcher = Agent(
            role='Email Researcher',
            goal='Analyze email content for key information and patterns',
            backstory='Expert at analyzing email communications and extracting insights'
        )
        
        summarizer = Agent(
            role='Email Summarizer',
            goal='Create concise summaries of email analysis',
            backstory='Specialist in creating actionable summaries from complex data'
        )

        # Create tasks
        analysis_results = []
        for email in emails:
            research_task = Task(
                description=f'Analyze email with subject: {email.subject}',
                agent=researcher
            )
            
            summary_task = Task(
                description='Create a summary of the analysis',
                agent=summarizer
            )

            # Create crew and run analysis
            crew = Crew(
                agents=[researcher, summarizer],
                tasks=[research_task, summary_task]
            )
            result = crew.kickoff()
            
            # Update database
            email.analyzed = True
            email.analysis_result = result
            analysis_results.append(result)
        
        self.session.commit()
        return analysis_results 