from pathlib import Path
import subprocess

def generate_diagrams():
    """Generate SVG diagrams from Mermaid definitions"""
    diagrams = {
        'package_dependencies': '''
        graph TD
            A[pyproject.toml] --> B[crews package]
            A --> C[timeline package]
            B --> D[base_crew.py]
            C --> D
            C --> E[analyzer_crew.py]
            D --> F[crewai]
            D --> G[langchain]
        ''',
        'project_structure': '''
        graph TD
            A[WORKSTATION] --> B[crews]
            A --> C[timeline]
            A --> D[DEV-MAN]
            B --> E[base_crew.py]
            B --> F[__init__.py]
            C --> G[analyzer_crew.py]
            C --> H[models.py]
            D --> I[diagrams]
            D --> J[docs]
        ''',
        'dependency_flow': '''
        graph TD
            A[Project Dependencies] --> B[Core]
            A --> C[Development]
            B --> D[crewai]
            B --> E[langchain]
            B --> F[sqlalchemy]
            C --> G[pytest]
            C --> H[black]
            C --> I[ruff]
        '''
    }
    
    output_dir = Path('DEV-MAN/diagrams/svg')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for name, definition in diagrams.items():
        output_file = output_dir / f"{name}.svg"
        
        # Use mmdc (Mermaid CLI) to generate SVG
        subprocess.run([
            'mmdc',
            '-i', '-',
            '-o', str(output_file),
            '-b', 'transparent'
        ], input=definition.encode())

if __name__ == "__main__":
    generate_diagrams() 