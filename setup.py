from setuptools import setup, find_packages

setup(
    name="rufus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.9.1',
        'beautifulsoup4>=4.12.2',
        'openai>=1.3.5',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered web scraper for RAG systems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rufus",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
