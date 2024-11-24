from setuptools import setup, find_packages

setup(
    name="wisdom_ex",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "yt-dlp>=2023.12.30",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "crewai>=0.1.0",
        "loguru>=0.7.2"
    ],
) 