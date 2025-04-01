from setuptools import setup, find_packages

setup(
    name="airflask",  
    version="0.6.0",
    author="Naitik Mundra",
    author_email="naitikmundra18@gmail.com",
    license="MIT",
    description="Simplest way to host your flask web app in production!",
    project_urls={
        "GitHub Repository": "https://github.com/naitikmundra/AirFlask"
    },
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(), 
    install_requires=[
        "flask",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "airflask=airflask.__main__:cli",  
        ],
    }

)
