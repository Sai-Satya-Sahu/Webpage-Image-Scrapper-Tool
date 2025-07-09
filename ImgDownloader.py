import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from mimetypes import guess_extension

SAVE_DIR = "downloaded_images"

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use updated headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--window-size=1920,3000")
    chrome_options.binary_location = "/usr/bin/chromium-broswer"
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def is_document_image(img_url, width, height):
    blacklist_keywords = ['logo', 'icon', 'ad', 'banner', 'favicon', 'avatar', 'button', 'share']
    if any(kw in img_url.lower() for kw in blacklist_keywords):
        return False
    return width >= 300 and height >= 300

def safe_download(url, retries=2, timeout=30):
    for attempt in range(retries + 1):
        try:
            return requests.get(url, timeout=timeout)
        except requests.exceptions.ReadTimeout:
            print(f"⚠️ Timeout on attempt {attempt+1} for {url}")
            time.sleep(3)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Connection error: {e}")
            break
    return None

def scroll_to_bottom_slowly(driver, max_checks=50):
    print("📜 Starting deep scroll to load all lazy images…")
    last_height = driver.execute_script("return document.body.scrollHeight")
    checks = 0

    while True:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1.5)

        # Force data-src to src if not yet triggered
        driver.execute_script("""
            document.querySelectorAll('img').forEach(img => {
                if (!img.src && img.dataset && img.dataset.src) {
                    img.src = img.dataset.src;
                }
            });
        """)

        new_height = driver.execute_script("return document.body.scrollHeight")
        checks += 1

        if new_height == last_height and checks >= max_checks:
            break
        last_height = new_height

    print("✅ Deep scroll complete. Final pause to let images load...")
    time.sleep(8)

def download_filtered_images(url):
    os.makedirs(SAVE_DIR, exist_ok=True)

    driver = setup_driver()
    driver.get(url)
    print(f"Opening page: {url}")

    print("⏳ Waiting 10 seconds for initial page render...")
    time.sleep(10)

    scroll_to_bottom_slowly(driver)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    images = soup.find_all("img")
    print(f"🔍 Found {len(images)} total <img> tags after full scroll.")

    count = 0
    for img in images:
        src = img.get("src") or img.get("data-src")
        if not src or src.lower().endswith(".svg"):
            continue

        img_url = urljoin(url, src)

        response = safe_download(img_url)
        if response is None:
            print(f"❌ Skipping: {img_url} (unreachable after retries)")
            continue

        try:
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            width, height = image.size

            if not is_document_image(img_url, width, height):
                continue

            content_type = response.headers.get("Content-Type", "")
            ext = guess_extension(content_type.split(";")[0]) or ".jpg"
            if not ext or ext.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"]:
                ext = ".jpg"

            file_name = os.path.join(SAVE_DIR, f"image_{count+1}{ext}")
            with open(file_name, "wb") as f:
                f.write(img_data)

            print(f"[{count+1}] Saved: {file_name}")
            count += 1

        except Exception as e:
            print(f"❌ Failed to save image {img_url}: {e}")

    print(f"\n✅ Done. {count} document images saved in '{SAVE_DIR}'.")

if __name__ == "__main__":
    print("📄 Document Image Downloader")
    input_url = input("🔗 Enter the full URL of the document page: ").strip()
    if not input_url.startswith("http"):
        print("❌ Invalid URL. Must start with http or https.")
    else:
        download_filtered_images(input_url)
