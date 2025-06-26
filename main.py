import json
import logging
from core.parser import get_ads
from constants.categories import BRAND_CATEGORIES


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    brand = input("Что ищем (бренд или название)? ").strip().lower()
    city_input = input("Город (например: Москва, Питер, Ростов): ").strip().lower()
    max_price = input("Максимальная цена (в рублях, можно оставить пустым): ").strip()

    category = None
    if brand in BRAND_CATEGORIES:
        print("Уточните категорию:")
        for idx, cat in enumerate(BRAND_CATEGORIES[brand].keys(), start=1):
            print(f"{idx}. {cat}")
        selected = input("Введите номер категории: ").strip()
        try:
            selected_idx = int(selected) - 1
            category = list(BRAND_CATEGORIES[brand].keys())[selected_idx]
        except:
            print("⚠ Категория не выбрана — поиск будет по всему сайту.")

    with_photos = input("Только с фото? (да/нет): ").strip().lower() == "да"

    results = get_ads(
        brand=brand,
        category=category,
        city_input=city_input,
        max_price=max_price,
        with_photos=with_photos
    )

    print(f"Найдено объявлений: {len(results)}")

    for ad in results:
        print(f"Название: {ad['title']}")
        print(f"Цена: {ad['price']}")
        print(f"Ссылка: {ad['link']}")
        print("-" * 40)

    with open("avito_result.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print("Готово, данные сохранены в avito_result.json")

if __name__ == "__main__":
    main()