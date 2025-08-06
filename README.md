
# SCRAPER

## Project Summary

SCRAPER is a Python-based web scraping framework that uses Selenium and Bright Data proxies to fetch web pages with rotating IP addresses. It automatically manages Chrome and ChromeDriver versions, and supports proxy authentication via a custom Chrome extension.

### Features
- Rotating proxies via Bright Data
- Selenium-based browser automation
- Automatic Chrome/ChromeDriver management
- Proxy authentication extension
- Easy integration and extensibility

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Create a `.env` file in the project root with your Bright Data credentials and required paths. Example:
     ```env
     BRIGHTDATA_USER=your_brightdata_username
     BRIGHTDATA_PASSWORD=your_brightdata_password
     BRIGHTDATA_PROXY_HOST=your_brightdata_proxy_host
     BRIGHTDATA_PROXY_PORT=your_brightdata_proxy_port
     CHROME_BINARY=/path/to/chrome
     ```
   - Download your Bright Data SSL certificate (`brightdata_certs.crt`) from the Bright Data dashboard and place it in the project root. This is required for secure proxy connections.

3. **Run the scraper test:**
   ```bash
   python test_selenium.py
   ```

## Main Components

- `root/services/selenium.py`: Manages Selenium WebDriver and Chrome/ChromeDriver setup.
- `root/services/brightdata.py`: Handles Bright Data proxy session and URL generation.
- `root/scrape.py`: Main `Scraper` class for fetching web pages.

## Example

```python
from root.scrape import Scraper

scraper = Scraper()
html = scraper.fetch('https://example.com')
print(html)
```

## Notes
- Chrome/ChromeDriver are managed automatically; manual setup scripts are not required.
- `.env` is ignored by git and should contain sensitive credentials only.
