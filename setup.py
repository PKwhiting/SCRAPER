from setuptools import setup, find_packages

setup(
    name="scraper",
    version="0.1.4",
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
    include_package_data=True,
    data_files=[('', ['setup_chrome.sh'])],
)