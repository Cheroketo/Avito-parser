from constants.categories import BRAND_CATEGORIES
from constants.cities import CITY_TRANSLATIONS
from constants.aliases import BRAND_ALIASES
import logging

logger = logging.getLogger(__name__)

def get_city():
    city_input = input("Город (например: Москва, Питер, Ростов): ").strip().lower()
    city = CITY_TRANSLATIONS.get(city_input)
    if not city:
        logger.warning(f"Город '{city_input}' не поддерживается. Используем Москву по умолчанию.")
        city = "moskva"
    return city

def get_brand_and_category():
    brand_input = input("Что ищем (бренд или название)? ").strip().lower()
    brand = BRAND_ALIASES.get(brand_input, brand_input)
    category_slug = ""

    if brand in BRAND_CATEGORIES:
        logger.info("Найдены категории для бренда. Запрос уточнения категории.")
        print("Уточните категорию:")
        for idx, cat in enumerate(BRAND_CATEGORIES[brand].keys(), start=1):
            print(f"{idx}. {cat}")

        selected = input("Введите номер категории: ").strip()
        if selected.isdigit():
            selected_idx = int(selected) - 1
            category_keys = list(BRAND_CATEGORIES[brand].keys())
            if 0 <= selected_idx < len(category_keys):
                category_name = category_keys[selected_idx]
                category_slug = BRAND_CATEGORIES[brand][category_name]
                logger.info(f"Выбрана категория: {category_name} (slug: {category_slug})")
            else:
                logger.warning("Некорректный номер категории — поиск по всему сайту.")
        else:
            logger.warning("Ввод не является числом — поиск по всему сайту.")
    return brand, category_slug
