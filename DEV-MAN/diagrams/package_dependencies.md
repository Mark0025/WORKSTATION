```mermaid
graph TD
    A[pyproject.toml] --> B[crews package]
    A --> C[timeline package]
    B --> D[base_crew.py]
    C --> D
    C --> E[analyzer_crew.py]
    D --> F[crewai]
    D --> G[langchain]
``` 