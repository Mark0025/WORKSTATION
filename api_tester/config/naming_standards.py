from typing import Dict
from loguru import logger

class APINameStandards:
    """Standardized naming conventions for APIs and services"""
    
    # Official API names and their standardized formats
    NAME_CORRECTIONS = {
        # AI and Language Models
        "OPENWEBUITEST": "OpenWebUI",
        "CURSORIDE": "CursorIDE",
        "OPENDEVIN": "OpenDevin",
        "GPTPILOT": "GPT-Pilot",
        "AUTOGENSTUDIO": "AutoGen Studio",
        "AIDERGPT": "Aider-GPT",
        "CREWAI": "CrewAI",
        "CREW-AI": "CrewAI",
        "CLAUDEAPI": "Claude API",
        "GROQ": "Groq",
        "DEEPGRAM": "DeepGram",
        
        # Infrastructure & Marketing
        "GHLMRKPLACE": "GoHighLevel",
        "UP2DATAPROPERTY": "Up2Date Property",
        "WEIVAITE": "Weaviate",
        "MAILGUN": "MailGun",
        "CLOUDFLARE": "Cloudflare",
        
        # Development & Tools
        "JIRA": "Jira",
        "GITHUB": "GitHub",
        "DOCKER": "Docker",
        "NOTION": "Notion",
        "ZOOM": "Zoom",
        "SLACK": "Slack",
        "TWILIO": "Twilio",
        
        # Search & APIs
        "SERPAPI": "SERP API",
        "HUGGINGFACE": "HuggingFace",
        "LANGCHAIN": "LangChain",
        "ZAPIER": "Zapier",
        
        # AI Platforms
        "SUPERAGI": "SuperAGI",
        "LHB": "LocalHouseBuyers"
    }
    
    # Platform categories for visualization
    PLATFORM_CATEGORIES = {
        "AI_SERVICES": [
            "OpenWebUI",
            "CursorIDE",
            "OpenDevin",
            "GPT-Pilot",
            "AutoGen Studio",
            "CrewAI",
            "Claude API",
            "Groq",
            "DeepGram",
            "HuggingFace",
            "LangChain",
            "SuperAGI"
        ],
        "INFRASTRUCTURE": [
            "Weaviate",
            "Cloudflare",
            "GoHighLevel"
        ],
        "MARKETING": [
            "Up2Date Property",
            "MailGun",
            "LocalHouseBuyers"
        ],
        "DEVELOPMENT": [
            "GitHub",
            "Docker",
            "Jira",
            "Notion"
        ],
        "COMMUNICATION": [
            "Slack",
            "Zoom",
            "Twilio"
        ],
        "SEARCH": [
            "SERP API",
            "Zapier"
        ]
    }
    
    # Status indicators
    STATUS_COLORS = {
        "active": "#10B981",     # Green
        "inactive": "#EF4444",   # Red
        "pending": "#F59E0B",    # Yellow
        "unknown": "#6B7280"     # Gray
    }

    @classmethod
    def standardize_name(cls, name: str) -> str:
        """Standardize an API name"""
        # Remove special characters and convert to uppercase for comparison
        clean_name = ''.join(c for c in name if c.isalnum()).upper()
        return cls.NAME_CORRECTIONS.get(clean_name, name)

    @classmethod
    def get_category(cls, name: str) -> str:
        """Get the category for a standardized API name"""
        std_name = cls.standardize_name(name)
        for category, apis in cls.PLATFORM_CATEGORIES.items():
            if std_name in apis:
                return category
        return "OTHER"

    @classmethod
    def get_status_color(cls, status: str) -> str:
        """Get the color for a status"""
        return cls.STATUS_COLORS.get(status, cls.STATUS_COLORS["unknown"])

    @classmethod
    def validate_name(cls, name: str) -> tuple:
        """Validate an API name and return correction if needed"""
        standard_name = cls.standardize_name(name)
        is_valid = standard_name != name
        return is_valid, standard_name