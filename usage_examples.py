#!/usr/bin/env python3
"""
AmzPy Advanced Usage Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example script demonstrates the enhanced features of AmzPy 0.2.0 including:
- Session configuration with curl_cffi
- Product details extraction
- Product searching with pagination
- Configuration options

Usage:
    python usage_curl_cffi.py
"""

from amzpy import AmazonScraper
import json
from pprint import pprint


def print_section(title):
    """Print a section header for cleaner output"""
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80 + "\n")


def example_product_detail():
    """Example: Fetching product details"""
    print_section("Product Details Example")
    
    # Create a basic scraper for Amazon India
    scraper = AmazonScraper(country_code="in")
    
    # Configure scraper with custom settings
    scraper.config('MAX_RETRIES = 3, REQUEST_TIMEOUT = 30')
    
    # Set a sample product URL
    url = "https://www.amazon.in/BATA-Mens-BOSS-Grass-Black-Loafer/dp/B08VJH1H55/"
    
    # Fetch and display product details
    print(f"Fetching details for: {url}\n")
    product = scraper.get_product_details(url)
    
    if product:
        print("\nProduct details successfully fetched:")
        # Display in a more organized format
        print(f"ASIN: {product.get('asin')}")
        print(f"Title: {product.get('title')}")
        print(f"Brand: {product.get('brand')}")
        print(f"Price: {product.get('currency', '')} {product.get('price')}")
        print(f"Rating: {product.get('rating')} / 5.0")
        print(f"Image URL: {product.get('img_url')}")
        
        # Save to JSON file for reference
        with open(f"product_{product.get('asin')}.json", "w") as f:
            json.dump(product, f, indent=2)
            print(f"\nFull details saved to product_{product.get('asin')}.json")
    else:
        print("Failed to fetch product details.")


def example_search():
    """Example: Searching for products"""
    print_section("Product Search Example")
    
    # Create a scraper with configuration and proxy (optional)
    scraper = AmazonScraper(
        country_code="in",
        impersonate="chrome119"
        # proxies={"http": "http://user:pass@proxy.example.com:8080"}  # Uncomment to use proxies
    )
    
    # Method 1: Search using a keyword query
    print("\n--- Method 1: Search by keyword ---")
    query = "wireless earbuds"
    print(f"Searching for: '{query}'")
    
    # Search with 2 pages of results
    products = scraper.search_products(query=query, max_pages=2)
    
    # Display the results
    if products:
        print(f"\nFound {len(products)} products:")
        for i, product in enumerate(products[:5], 1):  # Show first 5 products
            print(f"\n{i}. {product.get('title', 'N/A')}")
            print(f"   Price: {product.get('currency', '')} {product.get('price', 'N/A')}")
            print(f"   Rating: {product.get('rating', 'N/A')}")
            print(f"   ASIN: {product.get('asin', 'N/A')}")
        
        print(f"\n... and {len(products) - 5} more products")
        
        # Save to JSON file for reference
        with open("search_results.json", "w") as f:
            json.dump(products, f, indent=2)
            print(f"\nFull search results saved to search_results.json")
    else:
        print("No products found or search failed.")
    
    # Method 2: Search using a pre-constructed URL (e.g., for category pages)
    print("\n--- Method 2: Search using URL ---")
    search_url = "https://www.amazon.com/s?k=gaming+mouse&rh=n%3A172282%2Cp_36%3A2421888011"
    print(f"Searching with URL: {search_url}")
    
    # Limited to 1 page for demonstration
    category_products = scraper.search_products(search_url=search_url, max_pages=1)
    
    if category_products:
        print(f"\nFound {len(category_products)} products in category search")
        # Display a few details from the first product
        if category_products:
            first_product = category_products[0]
            print("\nFirst product details:")
            pprint(first_product)
    else:
        print("No products found in category search.")


def example_config():
    """Example: Demonstrating configuration options"""
    print_section("Configuration Example")
    
    # Create a scraper
    scraper = AmazonScraper()
    
    print("Default configuration:")
    print(scraper.user_config)
    
    # Method 1: Configure using string format
    print("\nUpdating with string configuration:")
    scraper.config('MAX_RETRIES = 5, REQUEST_TIMEOUT = 30, DELAY_BETWEEN_REQUESTS = (3, 8)')
    print(scraper.user_config)
    
    # Method 2: Configure using keyword arguments
    print("\nUpdating with keyword arguments:")
    scraper.config(MAX_RETRIES=4, DEFAULT_IMPERSONATE="safari15")
    print(scraper.user_config)


if __name__ == "__main__":
    # Uncomment the examples you want to run
    example_config()
    # example_product_detail()
    example_search()  # This may take longer to run 