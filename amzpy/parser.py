"""
Amazon HTML Parsing Module
~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains parsing functions for Amazon pages:
- Product detail pages (individual products)
- Search results pages (listings of products)

It uses BeautifulSoup to extract structured data from Amazon's HTML.
"""

import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import Dict, Optional, TYPE_CHECKING, Any, List, Tuple

# Using string annotation to avoid circular imports
if TYPE_CHECKING:
    from amzpy.session import AmzSession

from amzpy.utils import extract_brand_name


def parse_product_page(html_content: str, url: str = None, engine: Any = None, max_retries: int = 0) -> Optional[Dict]:
    """
    Parse Amazon product page HTML and extract structured product data.
    
    This function extracts key product information including:
    - Product title
    - Price and currency
    - Brand name
    - Product image URL
    
    Args:
        html_content (str): Raw HTML content of the product page
        url (str, optional): Product URL for reference
        engine (Any, optional): Legacy parameter, kept for backward compatibility
        max_retries (int): Legacy parameter, kept for backward compatibility
        
    Returns:
        Dict: Extracted product information 
        None: If parsing fails or HTML indicates a CAPTCHA/block
    """
    if not html_content:
        print("Error: Received empty HTML content")
        return None
        
    # Use lxml parser for better performance
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Check for CAPTCHA / Block Page before detailed parsing
    if "captcha" in html_content.lower() or "api-services-support@amazon.com" in html_content:
        print("Possible CAPTCHA or block page detected in HTML content")
        return None
    
    try:
        # Extract product title
        title_element = soup.select_one('#productTitle')
        title = title_element.text.strip() if title_element else None
        
        # Extract price information
        # We check multiple price selectors since Amazon's HTML structure varies
        price = None
        price_whole = soup.select_one('.a-price-whole')
        price_fraction = soup.select_one('.a-price-fraction')
        
        if price_whole:
            # Get whole number part
            price_text = price_whole.text.strip().replace(',', '')
            # Add decimal part if available
            if price_fraction:
                fraction_text = price_fraction.text.strip()
                price = float(f"{price_text}.{fraction_text}")
            else:
                price = float(price_text)
        
        # Alternative price selectors for different Amazon layouts
        if price is None:
            price_element = soup.select_one('span.a-offscreen')
            if price_element:
                price_text = price_element.text.strip()
                # Extract numeric value from price text (e.g., "$29.99" -> 29.99)
                price_match = re.search(r'[\d,]+\.?\d*', price_text)
                if price_match:
                    price = float(price_match.group().replace(',', ''))
        
        # Extract currency symbol
        currency_element = soup.select_one('.a-price-symbol')
        currency = currency_element.text.strip() if currency_element else None
        
        # Extract currency from alternate sources if first method fails
        if not currency and price is not None:
            price_element = soup.select_one('span.a-offscreen')
            if price_element:
                price_text = price_element.text.strip()
                currency_match = re.search(r'^[^\d]+', price_text)
                if currency_match:
                    currency = currency_match.group().strip()

        # Extract brand name
        brand_name = None
        brand_element = soup.select_one('#bylineInfo')
        if brand_element:
            brand_name = extract_brand_name(brand_element.text.strip())
            
        # Try alternative brand selectors if first method fails
        if not brand_name:
            # Try looking in the product details section
            detail_bullets = soup.select('#detailBullets_feature_div li')
            for bullet in detail_bullets:
                if 'brand' in bullet.text.lower():
                    brand_name = bullet.select_one('.a-text-bold + span')
                    if brand_name:
                        brand_name = brand_name.text.strip()
                    break
        
        # Extract main product image
        img_element = soup.select_one('#landingImage') or soup.select_one('#imgBlkFront')
        img_url = img_element.get('src') if img_element else None
        
        # Try to get high-resolution image URL if available
        if img_element and not img_url:
            data_old_hires = img_element.get('data-old-hires')
            data_a_dynamic_image = img_element.get('data-a-dynamic-image')
            
            if data_old_hires:
                img_url = data_old_hires
            elif data_a_dynamic_image:
                # This attribute contains a JSON string with multiple image URLs
                import json
                try:
                    image_dict = json.loads(data_a_dynamic_image)
                    # Get the URL with the highest resolution
                    if image_dict:
                        img_url = list(image_dict.keys())[0]
                except Exception:
                    pass
        
        # Extract ASIN (Amazon Standard Identification Number)
        asin = None
        if url:
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
            if asin_match:
                asin = asin_match.group(1)
                
        # Extract ratings if available
        rating = None
        rating_element = soup.select_one('#acrPopover') or soup.select_one('span.a-icon-alt')
        if rating_element:
            rating_text = rating_element.get('title', '') or rating_element.text
            rating_match = re.search(r'([\d\.]+)\s+out\s+of\s+5', rating_text)
            if rating_match:
                rating = float(rating_match.group(1))
        
        # Build the final product data dictionary
        product_data = {
            "title": title,
            "price": price,
            "img_url": img_url,
            "currency": currency,
            "brand": brand_name,
            "url": url,
            "asin": asin,
            "rating": rating
        }
        
        return product_data
        
    except Exception as e:
        print(f"Error parsing product page: {e}")
        return None


def parse_search_page(html_content: str, base_url: str = None) -> List[Dict]:
    """
    Parse Amazon search results page HTML and extract product listings.
    
    This function extracts a list of products from search or category pages:
    - Product title, URL, and ASIN
    - Price and currency
    - Thumbnail image
    - Ratings and review count when available
    - Prime eligibility
    
    Args:
        html_content (str): Raw HTML content of the search results page
        base_url (str, optional): Base URL for resolving relative URLs
        
    Returns:
        List[Dict]: List of extracted product data dictionaries
        Empty list: If parsing fails or HTML indicates a CAPTCHA/block
    """
    if not html_content:
        print("Error: Received empty HTML content for search page")
        return []
    
    # Use lxml parser for better performance on large search pages
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Check for CAPTCHA / Block Page before detailed parsing
    if "captcha" in html_content.lower() or "api-services-support@amazon.com" in html_content:
        print("CAPTCHA or block page detected in search results")
        return []
    
    # Prepare results list
    results = []
    
    try:
        # Try to locate search result containers
        # Amazon has multiple formats for search results, so we try several selectors
        product_containers = soup.select('div[data-component-type="s-search-result"]')
        
        # Alternative selector for some Amazon variants
        if not product_containers:
            product_containers = soup.select('.s-result-item')
        
        print(f"Found {len(product_containers)} potential product containers")
        
        # Process each product container
        for container in product_containers:
            try:
                # Skip sponsored listings if they don't have complete data
                if 'AdHolder' in container.get('class', []):
                    continue
                
                # Skip non-product containers (sometimes Amazon includes dividers, etc.)
                if 'asin' not in container.attrs:
                    continue
                
                # Extract product data
                product_data = {}
                
                # Get ASIN (Amazon Standard Identification Number)
                product_data['asin'] = container.get('data-asin') or container.get('asin')
                
                # Get product URL and title
                title_link = container.select_one('h2 a.a-link-normal') or container.select_one('.a-text-normal')
                if title_link:
                    product_data['title'] = title_link.text.strip()
                    href = title_link.get('href')
                    if href:
                        # Handle relative URLs
                        if href.startswith('/'):
                            product_data['url'] = urljoin(base_url, href) if base_url else href
                        else:
                            product_data['url'] = href
                
                # Get price
                price_element = container.select_one('.a-price .a-offscreen')
                if price_element:
                    price_text = price_element.text.strip()
                    # Parse price and currency
                    currency_match = re.search(r'^[^\d]+', price_text)
                    price_match = re.search(r'[\d,]+\.?\d*', price_text)
                    
                    if currency_match:
                        product_data['currency'] = currency_match.group().strip()
                    
                    if price_match:
                        product_data['price'] = float(price_match.group().replace(',', ''))
                
                # Get product image
                img_element = container.select_one('img.s-image')
                if img_element:
                    product_data['img_url'] = img_element.get('src')
                
                # Get ratings
                rating_element = container.select_one('i.a-icon-star-small')
                if rating_element:
                    rating_text = rating_element.text.strip()
                    rating_match = re.search(r'([\d\.]+)', rating_text)
                    if rating_match:
                        product_data['rating'] = float(rating_match.group(1))
                
                # Get review count
                reviews_element = container.select_one('span[aria-label*="reviews"]')
                if reviews_element:
                    reviews_text = reviews_element.get('aria-label', '')
                    reviews_match = re.search(r'([\d,]+)', reviews_text)
                    if reviews_match:
                        product_data['reviews_count'] = int(reviews_match.group(1).replace(',', ''))
                
                # Check for Prime eligibility
                prime_element = container.select_one('i.a-icon-prime')
                product_data['prime'] = bool(prime_element)
                
                # Add the product to our results list
                if product_data.get('title') and product_data.get('url'):
                    results.append(product_data)
                
            except Exception as e:
                print(f"Error parsing individual search result: {e}")
                continue  # Skip this item and continue with the next
        
        return results
        
    except Exception as e:
        print(f"Error parsing search page: {e}")
        return []


def parse_pagination_url(html_content: str, base_url: str = None) -> Optional[str]:
    """
    Extract the URL for the next page from search results pagination.
    
    Args:
        html_content (str): Raw HTML content of the search results page
        base_url (str, optional): Base URL for resolving relative URLs
        
    Returns:
        Optional[str]: URL of the next page, or None if there isn't one
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Try multiple selectors for pagination "Next" button
    next_link = (
        soup.select_one('a.s-pagination-next:not(.s-pagination-disabled)') or
        soup.select_one('li.a-last:not(.a-disabled) a') or
        soup.select_one('a:has(span:contains("Next"))')
    )
    
    if next_link and next_link.get('href'):
        next_url = next_link['href']
        # Handle relative URLs
        if next_url.startswith('/'):
            return urljoin(base_url, next_url) if base_url else next_url
        return next_url
    
    return None
