from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, GithubSearchTool, WebsiteSearchTool
from loguru import logger

class APIResearchCrew:
    def __init__(self):
        self.search_tool = SerperDevTool()
        self.github_tool = GithubSearchTool()
        self.web_tool = WebsiteSearchTool()

    def create_crew(self):
        # Create specialized agents
        github_researcher = Agent(
            role="GitHub API Researcher",
            goal="Find and analyze API repositories and documentation",
            tools=[self.github_tool],
            backstory="Expert at finding and analyzing GitHub repositories and API documentation"
        )

        api_analyst = Agent(
            role="API Security Analyst",
            goal="Analyze API security implications and automation possibilities",
            tools=[self.web_tool],
            backstory="Security expert specializing in API automation and security analysis"
        )

        integration_specialist = Agent(
            role="Integration Specialist",
            goal="Evaluate automation potential and integration challenges",
            tools=[self.search_tool],
            backstory="Expert in automated login systems and API integration"
        )

        tasks = [
            Task(
                description="""
                Research LastPass automation capabilities:
                1. Check if automated login is possible
                2. Identify potential security measures against automation
                3. Look for existing automation tools
                4. Document rate limiting and bot detection
                """,
                agent=api_analyst
            ),
            Task(
                description="""
                Analyze each API endpoint:
                1. Check GitHub for official SDKs
                2. Find authentication methods
                3. Document automation examples
                4. Identify common integration patterns
                """,
                agent=github_researcher
            ),
            Task(
                description="""
                Evaluate automation feasibility:
                1. Rate limiting analysis
                2. Bot detection mechanisms
                3. Legal implications
                4. Technical challenges
                """,
                agent=integration_specialist
            )
        ]

        return Crew(
            agents=[github_researcher, api_analyst, integration_specialist],
            tasks=tasks
        )

    async def analyze_automation_potential(self):
        """Run the crew to analyze automation potential"""
        crew = self.create_crew()
        results = await crew.kickoff()
        
        # Save findings
        self._save_analysis_report(results)
        return results

    def _save_analysis_report(self, results):
        """Save analysis results to a structured report"""
        with open("logs/automation_analysis.md", "w") as f:
            f.write("# API Automation Analysis Report\n\n")
            f.write("## LastPass Automation Potential\n")
            f.write(results.get("lastpass_analysis", "No analysis available"))
            f.write("\n\n## Security Considerations\n")
            f.write(results.get("security_analysis", "No analysis available"))
            f.write("\n\n## Technical Feasibility\n")
            f.write(results.get("technical_analysis", "No analysis available")) 