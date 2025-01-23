from typing import Tuple, Optional
import re

def parse_amazon_url(url: str) -> Optional[Tuple[str, str]]:
    """
    Parse Amazon product URL to extract base URL and product ID
    
    Args:
        url (str): Full Amazon product URL
        
    Returns:
        Tuple[str, str]: (base_url, product_id) if valid
        None: If URL is invalid
        
    Examples:
        >>> parse_amazon_url("https://www.amazon.com/dp/B0D4J2QDVY")
        ("https://www.amazon.com/", "B0D4J2QDVY")
        >>> parse_amazon_url("https://www.amazon.in/product-name/dp/B0D4J2QDVY/ref=...")
        ("https://www.amazon.in/", "B0D4J2QDVY")
    """
    # Clean up the URL
    url = url.strip()
    
    # Match Amazon domain and product ID
    pattern = r'https?://(?:www\.)?amazon\.([a-z.]+)(?:/[^/]+)*?/(?:dp|gp/product)/([A-Z0-9]{10})'
    match = re.search(pattern, url)
    
    if not match:
        return None
        
    # Extract domain and construct base URL
    domain = match.group(1)
    base_url = f"https://www.amazon.{domain}/"
    
    # Extract product ID
    product_id = match.group(2)
    
    return base_url, product_id 