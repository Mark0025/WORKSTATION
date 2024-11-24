from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from pathlib import Path
from loguru import logger
import json
import re

# Configure logger
logger.add(
    "wisdom-ex/logs/analyzer.log",
    rotation="500 MB",
    level="INFO",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
)

class WisdomAnalyzerCrew:
    def __init__(self, wisdom_dir):
        logger.info(f"Initializing WisdomAnalyzerCrew with directory: {wisdom_dir}")
        self.wisdom_dir = Path(wisdom_dir)
        self.metadata_file = self.wisdom_dir / "metadata.json"
        self.wisdom_file = self.wisdom_dir / "wisdom.md"
        
        # Initialize agents with logging
        logger.debug("Creating Research Analyst agent")
        self.researcher = Agent(
            role='Research Analyst',
            goal='Extract key themes and determine accurate title',
            backstory="""You are an expert at analyzing technical content and 
            identifying core themes. You specialize in understanding AI and 
            programming tutorials.""",
            tools=[self._create_read_file_tool()],
            verbose=True
        )
        
        logger.debug("Creating Metadata Specialist agent")
        self.metadata_specialist = Agent(
            role='Metadata Specialist',
            goal='Update metadata with accurate information',
            backstory="""You ensure metadata accuracy and completeness. You extract 
            key information from content and maintain proper JSON structure.""",
            tools=[self._create_update_metadata_tool()],
            verbose=True
        )
        
        logger.debug("Creating API Designer agent")
        self.api_designer = Agent(
            role='API Designer',
            goal='Create structured API from wisdom content',
            backstory="""You transform unstructured content into well-organized 
            API formats. You excel at creating clear, hierarchical JSON structures.""",
            tools=[self._create_create_api_tool()],
            verbose=True
        )

    def _create_read_file_tool(self):
        return Tool(
            name="read_wisdom_file",
            description="Read the contents of wisdom.md",
            func=lambda _: self.wisdom_file.read_text()
        )

    def _create_update_metadata_tool(self):
        return Tool(
            name="update_metadata",
            description="Update the metadata.json file",
            func=self._update_metadata
        )

    def _create_create_api_tool(self):
        return Tool(
            name="create_wisdom_api",
            description="Create structured wisdom.json API",
            func=self._create_wisdom_json
        )

    @logger.catch
    def analyze_wisdom(self):
        """Run the crew to analyze wisdom and update files"""
        logger.info("Starting wisdom analysis")
        
        try:
            # Create tasks
            logger.debug("Creating analysis tasks")
            analyze_task = Task(
                description="Analyze content and determine title",
                agent=self.researcher
            )

            metadata_task = Task(
                description="Update metadata with correct information",
                agent=self.metadata_specialist
            )

            api_task = Task(
                description="Create structured wisdom.json API",
                agent=self.api_designer
            )

            # Create and run crew
            logger.info("Initializing crew with agents and tasks")
            crew = Crew(
                agents=[self.researcher, self.metadata_specialist, self.api_designer],
                tasks=[analyze_task, metadata_task, api_task],
                verbose=True,
                process=Process.sequential
            )

            logger.info("Starting crew execution")
            result = crew.kickoff()
            
            # Update directory name if title changed
            logger.debug("Updating directory name based on analysis")
            self._update_directory_name()
            
            logger.success("Analysis completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error during wisdom analysis: {str(e)}")
            raise

    @logger.catch
    def _update_metadata(self, updates):
        """Update metadata.json with new information"""
        logger.info("Updating metadata.json")
        try:
            metadata = json.loads(self.metadata_file.read_text())
            metadata.update(json.loads(updates))
            self.metadata_file.write_text(json.dumps(metadata, indent=2))
            logger.success("Metadata updated successfully")
            return "Metadata updated successfully"
        except Exception as e:
            logger.error(f"Failed to update metadata: {str(e)}")
            raise

    @logger.catch
    def _create_wisdom_json(self, content):
        """Create structured wisdom.json API"""
        logger.info("Creating wisdom.json")
        try:
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

            api_structure = {
                "metadata": json.loads(self.metadata_file.read_text()),
                "content": sections,
                "relationships": {
                    "github_repos": [],
                    "references": sections.get("REFERENCES", []),
                    "related_topics": []
                }
            }

            wisdom_json_path = self.wisdom_dir / "wisdom.json"
            wisdom_json_path.write_text(json.dumps(api_structure, indent=2))
            logger.success("Wisdom API created successfully")
            return "Wisdom API created successfully"
        except Exception as e:
            logger.error(f"Failed to create wisdom.json: {str(e)}")
            raise

    def _update_directory_name(self):
        """Update directory name based on new title"""
        metadata = json.loads(self.metadata_file.read_text())
        if metadata["title"] != "unknown":
            new_dir_name = f"{metadata['title']}-{metadata['author']}-{metadata['date']}"
            new_dir_name = re.sub(r'[^\w\s-]', '', new_dir_name).strip().replace(' ', '-')
            new_dir = self.wisdom_dir.parent / new_dir_name
            if new_dir != self.wisdom_dir:
                self.wisdom_dir.rename(new_dir)

if __name__ == "__main__":
    logger.info("Starting WisdomAnalyzerCrew")
    crew = WisdomAnalyzerCrew("wisdom-ex/unknown-unknown-11-20-24")
    result = crew.analyze_wisdom()
    logger.info("Analysis complete!") 