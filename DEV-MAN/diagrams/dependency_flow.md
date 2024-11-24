```mermaid
graph TD
    A[Project Dependencies] --> B[Core]
    A --> C[Development]
    B --> D[crewai]
    B --> E[langchain]
    B --> F[sqlalchemy]
    C --> G[pytest]
    C --> H[black]
    C --> I[ruff]
``` 