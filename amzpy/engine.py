import requests
from typing import Optional
from fake_useragent import UserAgent

class RequestEngine:
    """Handles all HTTP requests to Amazon with anti-bot measures"""
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent(browsers=['Edge', 'Chrome'])
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
    def get(self, url: str) -> Optional[str]:
        """
        Make a GET request with anti-bot measures
        
        Args:
            url (str): URL to fetch
            
        Returns:
            str: HTML content if successful
            None: If request fails
        """
        try:
            # Update User-Agent for each request
            self.headers['User-Agent'] = self.ua.random
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception:
            return None
