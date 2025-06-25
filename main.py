import json
from playwright.sync_api import sync_playwright
from urllib.parse import quote
from constants.categories import BRAND_CATEGORIES
from constants.cities import CITY_TRANSLATIONS
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parser.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        brand = input("Что ищем (бренд или название)? ").strip().lower()
        city_input = input("Город (например: Москва, Питер, Ростов): ").strip().lower()
        max_price = input("Максимальная цена (в рублях, можно оставить пустым): ").strip()

        logger.info(f"Начало парсинга: бренд='{brand}', город='{city_input}', макс.цена='{max_price}'")

        # Перевод города
        city = CITY_TRANSLATIONS.get(city_input)
        if not city:
            logger.warning(f"Город '{city_input}' не поддерживается. Используем Москву по умолчанию.")
            city = "moskva"

        category_slug = ""
        if brand in BRAND_CATEGORIES:
            logger.info("Найдены категории для бренда. Запрос уточнения категории.")
            print("Уточните категорию:")
            for idx, cat in enumerate(BRAND_CATEGORIES[brand].keys(), start=1):
                print(f"{idx}. {cat}")

            selected = input("Введите номер категории: ").strip()
            try:
                selected_idx = int(selected) - 1
                category_name = list(BRAND_CATEGORIES[brand].keys())[selected_idx]
                category_slug = BRAND_CATEGORIES[brand][category_name]
                logger.info(f"Выбрана категория: {category_name} (slug: {category_slug})")
            except:
                logger.warning("Неверный выбор категории — поиск будет по всему сайту.")

        encoded_query = quote(brand)

        # Собираем URL
        if category_slug:
            url = f"https://www.avito.ru/{city}/{category_slug}?q={encoded_query}"
        else:
            url = f"https://www.avito.ru/{city}?q={encoded_query}"

        if max_price.isdigit():
            url += f"&pmax={max_price}"

        logger.info(f"Сформирован URL для парсинга: {url}")
        print(f"Ищу товары по ссылке: {url}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            logger.info("Открываем браузер и загружаем страницу...")
            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            logger.info("Ожидаем загрузки объявлений...")
            page.wait_for_selector('[data-marker="catalog-serp"]', timeout=60000)

            ads = page.locator('[data-marker="item"]')
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

                    logger.info(f"Обработано объявление {i+1}/{count}: {item_data['title']} - {item_data['price']}")
                    print(f"Название: {title}")
                    print(f"Цена: {price}")
                    print(f"Ссылка: https://www.avito.ru{link}")
                    print("-" * 40)

                except Exception as e:
                    logger.error(f"Ошибка при парсинге объявления {i}: {str(e)}", exc_info=True)

            # Сохраняем в JSON
            with open("avito.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logger.info(f"Парсинг завершен. Сохранено {len(data)} объявлений в файл avito_iphone.json")
            print("Готово, объявления сохранены!")
            browser.close()

    except Exception as e:
        logger.critical("Критическая ошибка в основном потоке", exc_info=True)
        print(f"Произошла критическая ошибка: {str(e)}")
        if 'browser' in locals():
            browser.close()

if __name__ == "__main__":
    main()