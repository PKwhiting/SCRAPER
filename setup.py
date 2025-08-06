from setuptools import setup, find_packages

setup(
    name="scraper_utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "requests",
        "langdetect",
        "backoff",
        "selenium",
        "python-dotenv",
        "webdriver-manager"
    ],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    author="PK Whiting",
    description="Utility functions for scraping",
    url="https://github.com/PKWhiting/SCRAPER",
)