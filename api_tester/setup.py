from setuptools import setup, find_packages

setup(
    name="api_tester",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "pytest",
        "pytest-asyncio",
        "loguru",
        "python-dotenv",
        "requests"
    ]
) 