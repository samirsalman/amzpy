# AmzPy - Amazon Product Scraper

AmzPy is a lightweight Python library for scraping product information from Amazon. It provides a simple interface to fetch product details like title, price, currency, and image URL while handling anti-bot measures automatically.

## Features

- Easy-to-use API for scraping Amazon product data
- Supports multiple Amazon domains (.com, .in, .co.uk, etc.)
- Built-in anti-bot protection
- Automatic retries on detection
- Clean and typed Python interface

## Installation

Install using pip:
`pip install amzpy`

## Usage

Here's a basic example of how to use AmzPy:

```python
from amzpy import AmazonScraper

scraper = AmazonScraper()
product_details = scraper.get_product_details("https://www.amazon.com/dp/B0D4J2QDVY")
print(product_details)
```

This will output the product details including title, price, image URL, and currency.

Feel free to explore the codebase for more details and advanced features. Happy scraping!

Output:
```json
{
"title": "Product Title",
"price": "299",
"currency": "$",
"img_url": "https://..."
}
```
## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- fake-useragent

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.