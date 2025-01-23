"""
The main scraper module for the Amazon Product API.
"""

from typing import Dict, Optional
from engine import RequestEngine
from parser import parse_product_page
from utils import parse_amazon_url

class AmazonScraper:
    """Main scraper class for Amazon product data"""
    
    def __init__(self, country_code: str = "com"):
        """Initialize the Amazon scraper"""
        self.base_url = f"https://www.amazon.{country_code}/"
        self.engine = RequestEngine()
    
    def get_product_details(self, url: str, max_retries: int = 3) -> Optional[Dict]:
        """
        Fetch details for a product using its Amazon URL
        
        Args:
            url (str): Amazon product URL
            max_retries (int): Maximum retry attempts if anti-bot measures detected
            
        Returns:
            Dict: Product details including title, price, img_url, and currency
            None: If URL is invalid or error occurs
        """
        parsed = parse_amazon_url(url)
        if not parsed:
            return None
            
        base_url, product_id = parsed
        
        # Construct product URL and get HTML
        product_url = f"{base_url}dp/{product_id}"
        html_content = self.engine.get(product_url)
        if not html_content:
            return None
            
        # Parse the product page and return the data
        return parse_product_page(html_content, product_url, self.engine, max_retries)
    
def main():
    scraper = AmazonScraper()
    url = "https://www.amazon.in/dp/B0D4J2QDVY"
    details = scraper.get_product_details(url, max_retries=5)
    print("Product details:", details)

if __name__ == "__main__":
    main()