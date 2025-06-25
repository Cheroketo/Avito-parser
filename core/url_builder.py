from urllib.parse import quote

def build_url(city, brand, category_slug, max_price, with_photo=False):

    encoded_query = quote(brand)
    if category_slug:
        url = f"https://www.avito.ru/{city}/{category_slug}?q={encoded_query}"
    else:
        url = f"https://www.avito.ru/{city}?q={encoded_query}"

    if max_price.isdigit():
        url += f"&pmax={max_price}"
    if with_photo:
        url += "&withImagesOnly=1"

    return url