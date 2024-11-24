from pathlib import Path
from src.extractor import WisdomExtractor

def main():
    extractor = WisdomExtractor()
    
    print("\n🧠 YouTube Wisdom Extractor 🧠\n")
    url = input("Enter YouTube URL: ")
    
    print("\nExtracting wisdom using Fabric...\n")
    wisdom, project_dir = extractor.extract_wisdom(url)
    
    if wisdom and project_dir:
        print("\n✨ Extraction Successful! ✨\n")
        print(f"Project created at: {project_dir}")
        print("\nProject structure:")
        print(f"└── {project_dir.name}/")
        print("    ├── README.md")
        print("    ├── wisdom.md")
        print("    └── project.json")
    else:
        print("\n❌ Failed to extract wisdom")

if __name__ == "__main__":
    main() 