# AmzPy - Amazon Product Scraper [![PyPI](https://img.shields.io/pypi/v/amzpy)](https://pypi.org/project/amzpy/)
![AmzPy Logo](https://i.imgur.com/QxrE60H.png)

<a href="https://www.producthunt.com/posts/amzpy?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-amzpy" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=812920&theme=neutral&t=1737654254074" alt="AmzPy - A&#0032;lightweight&#0032;Amazon&#0032;product&#0032;scraper&#0032;library&#0046; | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

AmzPy is a lightweight Python library for scraping product information from Amazon. It provides a simple interface to fetch product details like title, price, currency, and image URL while handling anti-bot measures automatically using curl_cffi for enhanced protection.

## Features

- Easy-to-use API for scraping Amazon product data
- Supports multiple Amazon domains (.com, .in, .co.uk, etc.)
- Enhanced anti-bot protection using curl_cffi with browser impersonation
- Automatic retries on detection with intelligent delay management
- Support for proxies to distribute requests
- Clean and typed Python interface

## Installation

Install using pip:
`pip install amzpy`

## Usage

Here's a basic example of how to use AmzPy:

```python
from amzpy import AmazonScraper

# Default configuration (amazon.com)
scraper = AmazonScraper()

# Or with custom configuration
# scraper = AmazonScraper(
#     country_code="in",
#     impersonate="chrome119",  # Browser to impersonate
#     proxies={"http": "http://user:pass@proxy.example.com:8080"}  # Optional proxies
# )

product_details = scraper.get_product_details("https://www.amazon.com/dp/B0D4J2QDVY")
print(product_details)
```

This will output the product details including title, price, image URL, currency, and brand.

Output:
```json
{
"title": "Product Title",
"price": 299,
"currency": "$",
"img_url": "https://...",
"brand": "BrandName"
}
```

## Requirements

- Python 3.6+
- curl_cffi (for enhanced anti-bot protection)
- beautifulsoup4
- lxml (for faster HTML parsing)

## Browser Impersonation

AmzPy uses curl_cffi's browser impersonation to mimic real browser requests, significantly improving success rates when scraping Amazon. By default, it impersonates Chrome 119, but you can specify other browsers when initializing the scraper.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.