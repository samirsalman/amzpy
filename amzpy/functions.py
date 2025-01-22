from bs4 import BeautifulSoup

def parse_product_details(html):
    soup = BeautifulSoup(html, "html.parser")

    # Extract the product title
    title_tag = soup.find("span", {"id": "productTitle"})
    title = title_tag.text.strip() if title_tag else "Title not found"

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
