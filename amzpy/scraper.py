from .engine import Engine
from .functions import parse_product_details

class AmazonScraper:
    def __init__(self, retries=3, delay=2):
        self.engine = Engine(retries=retries, delay=delay)

    def get_product_details(self, url, retries=3, delay=2):
        html = self.engine.request(url)
        return parse_product_details(html, retries, delay)
