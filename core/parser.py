import random
from core.browser_utils import random_human_delay

def parse_ads(page, logger):
    logger.info("Ожидаем загрузки объявлений...")
    page.wait_for_selector('[data-marker="catalog-serp"]', timeout=60000)
    page.wait_for_timeout(3000)

    page.mouse.move(random.randint(100, 800), random.randint(100, 600))
    page.mouse.wheel(0, random.randint(200, 800))
    random_human_delay()

    ads = page.locator('[data-marker="item"]')
    count = ads.count()
    if count == 0:
        ads = page.locator('div.iva-item-root-XBsVL')
        count = ads.count()

    logger.info(f"Найдено объявлений: {count}")
    print(f"Найдено объявлений: {count}")

    data = []
    for i in range(count):
        try:
            ad = ads.nth(i)
            title = ad.locator('[itemprop="name"]').inner_text()
            price = ad.locator('[data-marker="item-price"]').inner_text()
            link = ad.locator('a[data-marker="item-title"]').get_attribute("href")

            item_data = {
                "title": title.strip(),
                "price": price.strip(),
                "link": "https://www.avito.ru" + link.strip() if link else None
            }
            data.append(item_data)

            logger.info(f"Объявление {i+1}/{count}: {item_data['title']} - {item_data['price']}")
            print(f"Название: {title}\nЦена: {price}\nСсылка: https://www.avito.ru{link}\n" + "-" * 40)

            random_human_delay()

        except Exception as e:
            logger.error(f"Ошибка при парсинге объявления {i}: {str(e)}", exc_info=True)

    return data
