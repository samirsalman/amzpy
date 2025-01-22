from bs4 import BeautifulSoup
import time

def parse_product_details(html, retries=3, delay=2):
    """
    Parse the product details from the given HTML. Retry if the title is not found.

    Args:
        html (str): The HTML content of the Amazon product page.
        retries (int): Maximum number of retry attempts.
        delay (int): Delay (in seconds) between retries.

    Returns:
        dict: A dictionary containing product details (title, price, currency, img_url).
    """
    attempt = 0

    while attempt < retries:
        soup = BeautifulSoup(html, "html.parser")

        # Extract the product title
        title_tag = soup.find("span", {"id": "productTitle"})
        title = title_tag.text.strip() if title_tag else "Title not found"

        # If title is found, extract other details and return
        if title != "Title not found":
            # Extract the price
            price_tag = soup.find("span", {"class": "a-price-whole"})
            price = price_tag.text.strip() if price_tag else "Price not found"

            # Extract the currency
            currency_tag = soup.find("span", {"class": ""})
            currency = currency_tag.text.strip() if currency_tag else "Currency not found"

            # Extract the image URL
            img_tag = soup.find("img", {"id": "landingImage"})
            img_url = img_tag["src"] if img_tag else "Image URL not found"

            return {"title": title, "price": price, "currency": currency, "img_url": img_url}

        # Retry if title is not found
        attempt += 1
        if attempt < retries:
            print(f"Retrying... Attempt {attempt}/{retries}")
            time.sleep(delay)

    # If all retries fail, return a fallback response
    return {"error": "Failed to fetch valid product details after retries."}

