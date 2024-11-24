from crewai import Agent, Task, Crew
from pathlib import Path
import json
import re

class WisdomAnalyzerCrew:
    def __init__(self, wisdom_dir):
        self.wisdom_dir = Path(wisdom_dir)
        self.metadata_file = self.wisdom_dir / "metadata.json"
        self.wisdom_file = self.wisdom_dir / "wisdom.md"
        
        # Initialize agents
        self.researcher = Agent(
            role='Research Analyst',
            goal='Analyze wisdom content and extract key information',
            backstory="""You are an expert at analyzing content and extracting 
            meaningful insights. You excel at identifying main themes and topics.""",
            verbose=True
        )
        
        self.writer = Agent(
            role='Technical Writer',
            goal='Organize and structure information into clear formats',
            backstory="""You are skilled at organizing information into clear, 
            structured formats and creating comprehensive documentation.""",
            verbose=True
        )
        
        self.metadata_agent = Agent(
            role='Metadata Specialist',
            goal='Update and maintain accurate metadata',
            backstory="""You ensure all metadata is accurate, complete, and properly 
            formatted. You extract titles and key information from content.""",
            verbose=True
        )

    def analyze_wisdom(self):
        # Read current content
        wisdom_content = self.wisdom_file.read_text()
        metadata = json.loads(self.metadata_file.read_text())

        # Create tasks
        analyze_content = Task(
            description="""Analyze the wisdom.md content to extract:
            1. Main topic/title
            2. Key themes
            3. Core insights
            Use this to determine the proper title for the content.""",
            agent=self.researcher,
            context=wisdom_content
        )

        update_metadata = Task(
            description="""Update metadata.json with correct title and any additional 
            metadata based on the content analysis. Maintain existing fields.""",
            agent=self.metadata_agent,
            context=f"Current metadata: {json.dumps(metadata, indent=2)}"
        )

        organize_wisdom = Task(
            description="""Create a structured wisdom.json that organizes all insights 
            into a clear API format. Include:
            1. Title
            2. Summary
            3. Key themes
            4. Insights
            5. Recommendations
            6. References""",
            agent=self.writer
        )

        # Create crew
        crew = Crew(
            agents=[self.researcher, self.writer, self.metadata_agent],
            tasks=[analyze_content, update_metadata, organize_wisdom],
            verbose=True
        )

        # Execute crew tasks
        result = crew.kickoff()

        # Update files based on results
        self._update_files(result)
        
        return result

    def _update_files(self, analysis_result):
        # Extract new title and metadata updates
        new_title = self._extract_title(analysis_result)
        
        # Update metadata.json
        metadata = json.loads(self.metadata_file.read_text())
        metadata["title"] = new_title
        self.metadata_file.write_text(json.dumps(metadata, indent=2))

        # Create wisdom.json
        wisdom_json = self._create_wisdom_json(analysis_result)
        (self.wisdom_dir / "wisdom.json").write_text(
            json.dumps(wisdom_json, indent=2)
        )

        # Rename directory if title changed
        if metadata["title"] == "unknown":
            new_dir_name = f"{new_title}-{metadata['author']}-{metadata['date']}"
            new_dir_name = re.sub(r'[^\w\s-]', '', new_dir_name).strip().replace(' ', '-')
            new_dir = self.wisdom_dir.parent / new_dir_name
            self.wisdom_dir.rename(new_dir)

    def _extract_title(self, analysis_result):
        # Extract title from analysis result
        # This is a simplified version - enhance based on actual output format
        if "Voice Cloning Tutorial" in analysis_result:
            return "Voice-Cloning-Tutorial"
        return "AI-Voice-Cloning-Guide"

    def _create_wisdom_json(self, analysis_result):
        # Create structured JSON from wisdom content
        wisdom_content = self.wisdom_file.read_text()
        
        # Parse sections
        sections = {}
        current_section = None
        
        for line in wisdom_content.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].strip()
                sections[current_section] = []
            elif line.startswith('- ') and current_section:
                sections[current_section].append(line[2:])

        return {
            "title": self._extract_title(analysis_result),
            "sections": sections,
            "analysis": analysis_result
        }

if __name__ == "__main__":
    # Example usage
    crew = WisdomAnalyzerCrew("wisdom-ex/unknown-unknown-11-20-24")
    result = crew.analyze_wisdom()
    print("Analysis complete!")

