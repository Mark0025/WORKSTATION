from loguru import logger
import json
import os

def generate_docker_mermaid():
    """Generate Mermaid diagram for Docker services"""
    
    try:
        with open('docker_education.json', 'r') as f:
            data = json.load(f)
            
        # Create Mermaid diagram
        mermaid = """
graph TD
    subgraph Web[Web Layer]
        nginx[Nginx]:::active
        portainer[Portainer]:::active
    end

    subgraph Data[Data Layer]
        postgres[PostgreSQL]:::active
        redis[Redis]:::active
        mongodb[MongoDB]:::active
    end

    subgraph Queue[Message Queue]
        rabbitmq[RabbitMQ]:::active
    end

    subgraph Search[Search & Analytics]
        elastic[Elasticsearch]:::active
    end

    %% Connections
    nginx --> portainer
    nginx --> postgres
    nginx --> redis
    redis --> postgres
    rabbitmq --> mongodb
    elastic --> mongodb

    classDef active fill:#a7f3d0,stroke:#059669
    classDef pending fill:#fef3c7,stroke:#d97706
"""
        
        # Save Mermaid diagram
        with open('visualization/docker_services.html', 'w') as f:
            f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Docker Services Map</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold mb-8">Docker Services Map</h1>
        <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
            <div class="mermaid">
                {mermaid}
            </div>
        </div>
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose'
        }});
    </script>
</body>
</html>
""")
            
        logger.success("Docker services visualization generated")
        
    except Exception as e:
        logger.error(f"Error generating visualization: {str(e)}")

if __name__ == "__main__":
    generate_docker_mermaid() 