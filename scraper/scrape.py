from .services.selenium import SeleniumManager
from .services.brightdata import BrightDataService

class Scraper:

    def __init__(self):
        self.selenium_manager = SeleniumManager()
        self.bright_data_service = BrightDataService()

    def fetch(self, url):
        driver = self._get_driver()
        if not driver:
            raise Exception("Failed to initialize Selenium driver.")
        
        driver.get(url)
        return driver.page_source

    def _get_driver(self):
        return self._create_driver()
    
    def _create_driver(self):
        session_id = self.bright_data_service.generate_session_id()
        proxy_url = self.bright_data_service.get_proxy_url(session_id)
        driver = self.selenium_manager.get_driver(proxy_url=proxy_url)
        return driver