from setuptools import setup, find_packages

setup(
    name="crews",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "crewai==0.10.0",
        "langchain-openai==0.0.2",
        "langchain-community==0.0.24",
        "python-dotenv",
        "loguru==0.6.0",
        "duckduckgo-search",
        "fastapi",
        "uvicorn",
        "setuptools",
    ],
    entry_points={
        'console_scripts': [
            'run-crew=crews.run_all_crews:main',
            'run-viz=crews.visualization.server:main',
        ],
    }
) 