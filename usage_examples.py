#!/usr/bin/env python3
"""
AmzPy Advanced Usage Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example script demonstrates the enhanced features of AmzPy 0.2.0 including:
- Session configuration with curl_cffi
- Product details extraction
- Product searching with pagination
- Configuration options
- Enhanced search result parsing with color variants, discounts, and badges

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
    url = "https://www.amazon.in/Sparx-Mens-Red-Black-Flip-Flops/dp/B00IZ936HM/ref=sr_1_37?dib=eyJ2IjoiMSJ9.4xTlnBMWRsZUhc76GhsEgupJp7scFI1-LxWAaKnsBdUkKSFcwS5srU4Asgjnk3U73l841VhqU6DuRbOXQK7_HJ7UufcibD4L1WLcwEZSgmhSxgH--aqN5mp9fjrXRLbbPUIKKcqRN4KpPR-NEmcbGzKqpcSYKgAB9xfCEthgOjpjStXo7LLfKg5vuYALFuJjGiWgcHF3nJOXar4AHCRgSMFtiqQhAQmV_sr_c6rPKtk5YoGq1vn3SuaTNg6FeJiNOw5zNpavF7yS9zUFA0WU0BVve2y09CRdMw18fEqDQJk.zvtFkTh7TwTuQDwW4qBzr63RniJyBBeZjiDg86FATaM&dib_tag=se&qid=1744987780&refinements=p_6%3AA1WYWER0W24N8S%7CAWRHVFFS77KOB&rnid=1318474031&s=shoes&sr=1-37"
    
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
        print(f"Product URL: {product.get('url')}")
        
        # Save to JSON file for reference
        with open(f"product_{product.get('asin')}.json", "w") as f:
            json.dump(product, f, indent=2)
            print(f"\nFull details saved to product_{product.get('asin')}.json")
    else:
        print("Failed to fetch product details.")


def example_search_by_query(query: str = None):
    """Example: Searching for products with enhanced parsing"""
    print_section("Enhanced Product Search Example")
    
    # Create a scraper with configuration
    scraper = AmazonScraper(
        country_code="in",
        impersonate="chrome119"
    )
    
    # Method 1: Search for shoes on Amazon India 
    print("\n--- Method 1: Enhanced Search by Keyword ---")
    print(f"Searching for: '{query}' on Amazon India")
    
    # Search with 5 pages of results for demonstration
    products = scraper.search_products(query=query, max_pages=5)
    
    # Display the enhanced results
    if products:
        print(f"\nFound {len(products)} products:")
        
        # Show more detailed information for the first few products
        detailed_count = min(3, len(products))
        for i, product in enumerate(products[:detailed_count], 1):
            print(f"\n{i}. {product.get('title', 'N/A')}")
            print(f"   Brand: {product.get('brand', 'N/A')}")
            print(f"   Price: {product.get('currency', '')} {product.get('price', 'N/A')}")
            print(f"   URL: {product.get('url')}")  # This will now be in canonical format
            
            # Display discount information if available
            if 'original_price' in product:
                print(f"   Original Price: {product.get('currency', '')} {product.get('original_price')}")
                print(f"   Discount: {product.get('discount_percent', 'N/A')}% off")
            
            # Display ratings and reviews
            if 'rating' in product:
                print(f"   Rating: {product.get('rating')} / 5.0 ({product.get('reviews_count', 0)} reviews)")
            
            # Display color variants if available
            if 'color_variants' in product:
                variant_count = len(product['color_variants'])
                print(f"   Available in {variant_count} colors:")
                for v in product['color_variants'][:3]:
                    print(f"     - {v['name']}: {v['url']}")
                if variant_count > 3:
                    print(f"     - ...and {variant_count-3} more colors")
            
            # Display badge information if available
            if 'badge' in product:
                print(f"   Badge: {product.get('badge')}")
                
            # Display Prime eligibility
            prime_status = "Yes" if product.get('prime', False) else "No"
            print(f"   Prime Eligible: {prime_status}")
            
            # Display delivery information
            if 'delivery_info' in product:
                print(f"   Delivery: {product.get('delivery_info')}")
                
            # Display ASIN
            print(f"   ASIN: {product.get('asin', 'N/A')}")
            
        # Show summary for remaining products
        if len(products) > detailed_count:
            print(f"\n... and {len(products) - detailed_count} more products")
        
        # Save all results to JSON for reference
        with open("enhanced_search_results.json", "w") as f:
            json.dump(products, f, indent=2)
            print(f"\nFull search results saved to enhanced_search_results.json")
    else:
        print("No products found or search failed.")


def example_search_by_url(url, max_pages: int = 5):
    """Example: Searching for products with enhanced parsing"""
    print_section("Enhanced Product Search Example")
    
    # Create a scraper with configuration
    scraper = AmazonScraper(
        country_code="in",
        impersonate="chrome119"
    )
    
    # Method 2: Search using a pre-constructed URL
    print(f"\n--- Method 2: Enhanced Search by URL ---")
    print(f"Searching with URL: {url}")
    
    # Search with 5 pages of results for demonstration
    products = scraper.search_products(search_url=url, max_pages=max_pages)
    
    # Display the enhanced results
    if products:
        print(f"\nFound {len(products)} products:")
        
        # Show more detailed information for the first few products
        detailed_count = min(3, len(products))
        for i, product in enumerate(products[:detailed_count], 1):
            print(f"\n{i}. {product.get('title', 'N/A')}")
            print(f"   Brand: {product.get('brand', 'N/A')}")
            print(f"   Price: {product.get('currency', '')} {product.get('price', 'N/A')}")
            print(f"   URL: {product.get('url')}")  # This will now be in canonical format
            
            # Display discount information if available
            if 'original_price' in product:
                print(f"   Original Price: {product.get('currency', '')} {product.get('original_price')}")
                print(f"   Discount: {product.get('discount_percent', 'N/A')}% off")
            
            # Display ratings and reviews
            if 'rating' in product:
                print(f"   Rating: {product.get('rating')} / 5.0 ({product.get('reviews_count', 0)} reviews)")
            
            # Display color variants if available
            if 'color_variants' in product:
                variant_count = len(product['color_variants'])
                print(f"   Available in {variant_count} colors:")
                for v in product['color_variants'][:3]:
                    print(f"     - {v['name']}: {v['url']}")
                if variant_count > 3:
                    print(f"     - ...and {variant_count-3} more colors")
            
            # Display badge information if available
            if 'badge' in product:
                print(f"   Badge: {product.get('badge')}")
                
            # Display Prime eligibility
            prime_status = "Yes" if product.get('prime', False) else "No"
            print(f"   Prime Eligible: {prime_status}")
            
            # Display delivery information
            if 'delivery_info' in product:
                print(f"   Delivery: {product.get('delivery_info')}")
                
            # Display ASIN
            print(f"   ASIN: {product.get('asin', 'N/A')}")
            
        # Show summary for remaining products
        if len(products) > detailed_count:
            print(f"\n... and {len(products) - detailed_count} more products")
        
        # Save all results to JSON for reference
        with open("enhanced_search_results_by_url.json", "w") as f:
            json.dump(products, f, indent=2)
            print(f"\nFull search results saved to enhanced_search_results_by_url.json")
    else:
        print("No products found or search failed.")


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
    # example_config()
    example_product_detail()
    # example_search_by_query("men sneakers size 9")  # Show the enhanced search capabilities 
    # example_search_by_url("https://www.amazon.in/s?i=shoes&rh=n%3A1983518031%2Cp_6%3AA1WYWER0W24N8S%257CAWRHVFFS77KOB&s=popularity-rank&dc&fs=true&qid=1744987773&rnid=1318474031&ref=sr_nr_p_6_5&ds=v1%3AA6W8CK0Zg%2BT79cnzjqg%2BNAW97tG2vkGoOGtBupouOe8", max_pages=200)