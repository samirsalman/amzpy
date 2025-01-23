from bs4 import BeautifulSoup
from typing import Dict, Optional
from engine import RequestEngine

def parse_product_page(html_content: str, url: str = None, engine: RequestEngine = None, max_retries: int = 0) -> Optional[Dict]:
    """
    Parse Amazon product page HTML and extract relevant information
    
    Args:
        html_content (str): Raw HTML content of the product page
        url (str, optional): Product URL for retrying if needed
        engine (RequestEngine, optional): RequestEngine instance for retries
        max_retries (int): Number of remaining retry attempts
        
    Returns:
        Dict: Extracted product information (title, price, img_url, currency)
        None: If parsing fails after all retries
    """
    if not html_content:
        return None
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    try:
        # Get title
        title = soup.select_one('#productTitle')
        title = title.text.strip() if title else None
        
        # If title is None and we have retries left, try again
        if title is None and max_retries > 0 and url and engine:
            print(f"Retry attempt {max_retries} - Anti-bot measure detected")
            new_html = engine.get(url)
            return parse_product_page(new_html, url, engine, max_retries - 1)
        
        # Get price
        price_element = soup.select_one('.a-price-whole')
        price = price_element.text.strip().replace(',', '') if price_element else None
        
        # Get currency symbol
        currency_element = soup.select_one('.a-price-symbol')
        currency = currency_element.text.strip() if currency_element else None
        
        # Get main product image
        img_element = soup.select_one('#landingImage') or soup.select_one('#imgBlkFront')
        img_url = img_element.get('src') if img_element else None
        
        return {
            "title": title,
            "price": price,
            "img_url": img_url,
            "currency": currency
        }
    except Exception:
        # If we have retries left, try again
        if max_retries > 0 and url and engine:
            print(f"Retry attempt {max_retries} - Error occurred")
            new_html = engine.get(url)
            return parse_product_page(new_html, url, engine, max_retries - 1)
        return None
