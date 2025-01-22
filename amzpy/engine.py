import requests
from fake_useragent import UserAgent
import time

class Engine:
    def __init__(self, retries=3, delay=2):
        self.session = requests.Session()
        self.ua = UserAgent(browsers=["Edge", "Chrome"])
        self.retries = retries
        self.delay = delay
        self.session.headers.update({"Accept-Language": "en-US,en;q=0.9"})

    def _get_headers(self):
        return {"User-Agent": self.ua.random}

    def request(self, url):
        for attempt in range(self.retries):
            try:
                self.session.headers.update(self._get_headers())
                response = self.session.get(url)
                if response.status_code == 200:
                    return response.text
                else:
                    raise Exception(f"Failed to fetch page. Status code: {response.status_code}")
            except Exception as e:
                if attempt < self.retries - 1:
                    time.sleep(self.delay)
                else:
                    raise e
