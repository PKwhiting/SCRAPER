import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import zipfile
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import zipfile
import re
class SeleniumManager:
    def __init__(self, ):
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

    def start_driver(self, proxy_url=None, headless=True):
        if self.driver is not None and self.current_proxy != proxy_url:
            self.close()

        if self.driver is None:
            try:
                chrome_options = Options()
                if headless:
                    chrome_options.add_argument("--headless=new")  # Use new headless mode for Chromium 109+
                chrome_options.add_argument("--headless=new")  # Use new headless mode for Chromium 109+
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--remote-debugging-port=9222")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                # Set Chrome binary location from .env
                chrome_binary = os.getenv("CHROME_BINARY")
                chrome_version = None
                if chrome_binary:
                    chrome_options.binary_location = chrome_binary
                    # Get Chrome version from binary
                    import subprocess
                    try:
                        version_output = subprocess.check_output([chrome_binary, "--version"]).decode()
                        # Example output: 'Google Chrome 139.0.7258.66\n'
                        import re
                        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', version_output)
                        if match:
                            chrome_version = match.group(1)
                    except Exception as e:
                        logging.getLogger(__name__).warning(f"Could not determine Chrome version: {e}")

                if proxy_url:
                    self.proxy_extension_zip = self._create_proxy_extension(proxy_url)
                    chrome_options.add_extension(self.proxy_extension_zip)

                if chrome_version:
                    service = Service(ChromeDriverManager(driver_version=chrome_version).install())
                else:
                    service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.current_proxy = proxy_url
                logging.getLogger(__name__).info(f"Chrome driver started successfully (Proxy: {proxy_url or 'None'})")
            except Exception as e:
                logging.getLogger(__name__).error(f"Failed to start Chrome driver: {str(e)}")
                raise
        return self.driver

    def get_driver(self, proxy_url=None, headless=True):
        return self.start_driver(proxy_url=proxy_url, headless=headless)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.current_proxy = None
            if self.proxy_extension_zip and os.path.exists(self.proxy_extension_zip):
                os.remove(self.proxy_extension_zip)
                self.proxy_extension_zip = None
