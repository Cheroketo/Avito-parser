# main.py
import logging
import sys
from playwright.sync_api import sync_playwright
from core.input_handlers import get_city, get_brand_and_category
from core.url_builder import build_url
from core.browser_utils import prepare_browser, random_human_delay
from core.parser import parse_ads

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
        brand, category_slug = get_brand_and_category()
        city = get_city()
        max_price = input("Максимальная цена (в рублях, можно оставить пустым): ").strip()

        with_photo_input = input("Показывать только объявления с фото? (да/нет): ").strip().lower()
        with_photo = with_photo_input in ["да", "д", "yes", "y"]

        logger.info(f"Начало парсинга: бренд='{brand}', город='{city}', макс.цена='{max_price}', фото только='{with_photo}'")
        url = build_url(city, brand, category_slug, max_price, with_photo)

        logger.info(f"Сформирован URL для парсинга: {url}")
        print(f"Ищу товары по ссылке: {url}")

        with sync_playwright() as p:
            browser, page = prepare_browser(p, url)
            data = parse_ads(page, logger)

            with open("avito.json", "w", encoding="utf-8") as f:
                import json
                json.dump(data, f, ensure_ascii=False, indent=4)

            logger.info(f"Парсинг завершен. Сохранено {len(data)} объявлений в avito.json")
            print("Готово, объявления сохранены!")
            browser.close()

    except Exception as e:
        logger.critical("Критическая ошибка в основном потоке", exc_info=True)
        print(f"Произошла критическая ошибка: {str(e)}")
        if 'browser' in locals():
            browser.close()

if __name__ == "__main__":
    main()
