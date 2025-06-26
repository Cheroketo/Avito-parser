
import logging
from urllib.parse import quote
from constants.categories import BRAND_CATEGORIES
from constants.cities import CITY_TRANSLATIONS
from core.browser_utils import launch_and_get_page, random_human_delay


def get_ads(brand, category=None, city_input="москва", max_price="", with_photos=False, pages=1):
    logger = logging.getLogger(__name__)
    city = CITY_TRANSLATIONS.get(city_input.lower())
    if not city:
        logger.warning(f"Неизвестный город '{city_input}', используется 'moskva'")
        city = "moskva"

    encoded_query = quote(brand)
    category_slug = BRAND_CATEGORIES.get(brand, {}).get(category, "")

    if category_slug:
        url = f"https://www.avito.ru/{city}/{category_slug}?q={encoded_query}"
    else:
        url = f"https://www.avito.ru/{city}?q={encoded_query}"

    if max_price.isdigit():
        url += f"&pmax={max_price}"

    if with_photos:
        url += "&withImagesOnly=1"

    logger.info(f"Парсим URL: {url}")

    try:
        browser, page = launch_and_get_page(url)
        page.wait_for_selector('[data-marker="catalog-serp"]', timeout=60000)
        ads = page.locator('[data-marker="item"]')

        count = ads.count()
        results = []

        for i in range(count):
            try:
                ad = ads.nth(i)
                title = ad.locator('[itemprop="name"]').inner_text()
                price = ad.locator('[data-marker="item-price"]').inner_text()
                link = ad.locator('a[data-marker="item-title"]').get_attribute("href")
                results.append({
                    "title": title.strip(),
                    "price": price.strip(),
                    "link": f"https://www.avito.ru{link.strip()}"
                })
                random_human_delay(0.3, 0.8)
            except Exception as e:
                logger.warning(f"Ошибка парсинга объявления {i}: {e}")

        browser.close()
        return results

    except Exception as e:
        logger.error(f"Не удалось получить данные: {e}")
        return []

