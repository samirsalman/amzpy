import unittest
from amzpy.scraper import AmazonScraper

class TestAmazonScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = AmazonScraper(retries=1, delay=1)

    def test_product_details(self):
        url = "https://www.amazon.in/dp/B09JK1PZ7N"
        result = self.scraper.get_product_details(url)
        self.assertIn("title", result)
        self.assertIn("price", result)

if __name__ == "__main__":
    unittest.main()
