from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool

# Create a simple tool
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="web_search",
        func=search.run,
        description="Search the web for information"
    )
]

# Create a test agent
test_agent = Agent(
    role="Researcher",
    goal="Research a topic",
    backstory="You are a researcher who finds information.",
    tools=tools,
    verbose=True
)

# Create a test task
test_task = Task(
    description="Search for information about CrewAI",
    agent=test_agent
)

# Create crew
crew = Crew(
    agents=[test_agent],
    tasks=[test_task]
)

if __name__ == "__main__":
    result = crew.kickoff()
    print(result) 