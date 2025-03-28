from setuptools import setup, find_packages

setup(
    name="airflask",  
    version="0.0.1",
    author="Naitik Mundra",
    author_email="naitikmundra18@gmail.com",
    description="Simplest way to host your flask web app in production!",
    url="https://github.com/naitikmundra/AirFlask",
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
