from amzpy.scraper import AmazonScraper

def main():
    scraper = AmazonScraper()
    url = "https://www.amazon.in/dp/B0D4J2QDVY"
    details = scraper.get_product_details(url, max_retries=5)
    print("Product details:", details)

if __name__ == "__main__":
    main()