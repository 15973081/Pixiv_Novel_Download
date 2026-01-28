import requests
from ..core.config import app_config

class HttpClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HttpClient, cls).__new__(cls)
            cls._instance.session = requests.Session()
            cls._instance._configure_session()
        return cls._instance
    
    def _configure_session(self):
        # Set headers
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.pixiv.net/",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        
        # Set auth cookie if available
        cookie = app_config.get("auth", {}).get("cookie")
        if cookie:
            self.session.headers.update({"Cookie": cookie})
            
        # Set proxy if available and enabled
        proxy_config = app_config.get("proxy", {})
        if proxy_config.get("enabled", False):
            proxies = {
                k: v for k, v in proxy_config.items() 
                if k in ["http", "https"] and v
            }
            if proxies:
                self.session.proxies.update(proxies)

    def get(self, url, params=None, **kwargs):
        return self.session.get(url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.session.post(url, data=data, json=json, **kwargs)

    def update_cookie(self, cookie: str):
        self.session.headers.update({"Cookie": cookie})
        # Update config in memory (persisting to file is optional but recommended for UX)
        app_config["auth"]["cookie"] = cookie

# Singleton instance
http_client = HttpClient()
