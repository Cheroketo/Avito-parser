import random
import time

def random_human_delay(min_sec=2.5, max_sec=5.0):
    time.sleep(random.uniform(min_sec, max_sec))

def prepare_browser(playwright, url):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800}
    )
    page = context.new_page()
    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    return browser, page
