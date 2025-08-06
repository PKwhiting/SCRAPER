from bs4 import BeautifulSoup
import requests
from django.conf import settings
import time
import random
from langdetect import detect, LangDetectException
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import backoff

class BrightDataService:
    def __init__(self, max_retries=5, base_delay=2, max_delay=10):
        self.username = settings.BRIGHTDATA_USERNAME
        self.password = settings.BRIGHTDATA_PASSWORD
        self.port = 33335
        self.cert_path = settings.BRIGHTDATA_CERT_PATH
        # Always use http:// in the proxy URL, even for https requests (as per their example)
        self.proxy_url = f'http://{self.username}:{self.password}@brd.superproxy.io:{self.port}'
        
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.desired_language = 'en-US'

    def get_proxy_url(self, session_id):
        return self.proxy_url.format(
            username=self.username,
            session_id=session_id,
            password=self.password,
            port=self.port
        )

    @backoff.on_exception(backoff.expo, 
                          (requests.exceptions.RequestException, requests.exceptions.Timeout),
                          max_tries=5)
    def fetch_url(self, url, session_id=None):
        if session_id is None:
            session_id = self.generate_session_id()
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
        
        proxy_url = self.get_proxy_url(session_id)
        proxies = {
            'http': proxy_url,
            'https': proxy_url,
        }
        
        try:
            response = requests.get(url, proxies=proxies, headers=headers, timeout=30, verify=self.cert_path)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}. Retrying with a new session...")
            # Generate a new session ID for the next attempt
            session_id = self.generate_session_id()
            raise  # Re-raise the exception to trigger the backoff retry

    def generate_session_id(self):
        return random.randint(1, 100000)

    def is_english(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        html_tag = soup.find('html')
        
        if html_tag and 'lang' in html_tag.attrs:
            return html_tag['lang'].startswith('en')
        
        # Detect language using langdetect
        try:
            detected_language = detect(content)
            return detected_language.startswith('en')
        except LangDetectException:
            return False

