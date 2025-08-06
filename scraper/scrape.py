from .services import SeleniumManager
from .services import BrightDataService
from selenium import webdriver

class Scraper:

    def __init__(self, headless=True):
        self.selenium_manager = SeleniumManager()
        self.bright_data_service = BrightDataService()
        self.headless = headless

    def fetch(self, url) -> webdriver.Chrome:
        driver = self._get_driver()
        if not driver:
            raise Exception("Failed to initialize Selenium driver.")
        
        driver.get(url)
        return driver

    def _get_driver(self):
        return self._create_driver()
    
    def _create_driver(self):
        session_id = self.bright_data_service.generate_session_id()
        proxy_url = self.bright_data_service.get_proxy_url(session_id)
        driver = self.selenium_manager.get_driver(proxy_url=proxy_url, headless=self.headless)
        return driver