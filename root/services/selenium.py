import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import zipfile
import re

logger = logging.getLogger(__name__)

class SeleniumManager:


    def __init__(self):
        self.driver = None
        self.current_proxy = None
        self.proxy_extension_zip = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _create_proxy_extension(self, proxy_url):
        """Creates a Chrome extension to handle proxy authentication."""
        if not proxy_url:
            return None
        
        # Extract user, pass, host, and port from proxy_url
        proxy_parts = re.match(r'http://(.*?):(.*?)@(.*?):(\d+)', proxy_url)
        if not proxy_parts:
            raise ValueError("Invalid proxy URL format. Expected http://user:pass@host:port")
        
        username, password, host, port = proxy_parts.groups()

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            }
        }
        """

        background_js = f"""
        var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{host}",
                    port: parseInt({port})
                }},
                bypassList: ["localhost"]
            }}
        }};

        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

        function callbackFn(details) {{
            return {{
                authCredentials: {{
                    username: "{username}",
                    password: "{password}"
                }}
            }};
        }}

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {{urls: ["<all_urls>"]}},
            ['blocking']
        );
        """
        
        extension_path = 'proxy_auth_extension.zip'
        with zipfile.ZipFile(extension_path, 'w') as zf:
            zf.writestr("manifest.json", manifest_json)
            zf.writestr("background.js", background_js)
            
        return extension_path

    def start_driver(self, proxy_url=None):
        if self.driver is not None and self.current_proxy != proxy_url:
            self.close()

        if self.driver is None:
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                
                if proxy_url:
                    self.proxy_extension_zip = self._create_proxy_extension(proxy_url)
                    chrome_options.add_extension(self.proxy_extension_zip)
                
                chrome_binary = os.environ.get('CHROME_BINARY')
                if chrome_binary:
                    chrome_options.binary_location = chrome_binary

                chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
                service = Service(executable_path=chromedriver_path)
                
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.current_proxy = proxy_url
                logger.info(f"Chrome driver started successfully (Proxy: {proxy_url or 'None'})")
            except Exception as e:
                logger.error(f"Failed to start Chrome driver: {str(e)}")
                raise
        return self.driver

    def get_driver(self, proxy_url=None):
        return self.start_driver(proxy_url=proxy_url)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.current_proxy = None
            if self.proxy_extension_zip and os.path.exists(self.proxy_extension_zip):
                os.remove(self.proxy_extension_zip)
                self.proxy_extension_zip = None
