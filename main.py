from playwright.sync_api import sync_playwright
import json
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page()

        # Устанавливаем User-Agent
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        try:
            # Переходим на мобильную версию
            page.goto("https://m.avito.ru",  timeout=60000)

            # Ждём немного для прогрузки контента
            time.sleep(5)

            # Прокручиваем страницу вниз (эмуляция поведения пользователя)
            for _ in range(3):
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                time.sleep(2)

            # Находим блоки с объявлениями
            ads = page.locator(".item.item_table")

            # Создаём список для хранения данных
            data = []

            # Проходим по каждому объявлению
            for ad in ads.all():
                try:
                    title = ad.locator(".snippet-title").inner_text(timeout=5000)
                    price = ad.locator(".snippet-price-row").inner_text(timeout=5000)
                    link = ad.locator(".snippet-link").get_attribute("href", timeout=5000)
                    full_link = f"https://m.avito.ru{link}"  if link.startswith("/") else link

                    data.append({
                        "title": title.strip(),
                        "price": price.strip(),
                        "link": full_link
                    })
                except Exception as e:
                    print("Ошибка при парсинге одного объявления:", e)

            # Сохраняем данные в JSON
            with open("avito_ads.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Сохранено {len(data)} объявлений в файл avito_ads.json")

        except Exception as e:
            print("Ошибка:", e)
        finally:
            browser.close()

if __name__ == "__main__":
    main()