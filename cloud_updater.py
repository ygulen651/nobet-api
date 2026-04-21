import requests
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Yapılandırma
RENDER_URL = os.environ.get("RENDER_API_URL", "https://nobet-eczane-api.onrender.com/api/update")
PA_URL = "https://yusuf7007.pythonanywhere.com/api/update"
TARGET_APIS = [RENDER_URL, PA_URL]
NOBET_URL = "https://www.karamaneo.org.tr/nobet-listesi"

def fetch_with_requests():
    """Selenium engellenirse düz requests ile dene"""
    print("Yedek mkanizma: Requests ile deneniyor...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(NOBET_URL, headers=headers, timeout=20)
        if r.status_code == 200 and len(r.text) > 5000:
            return r.text
    except:
        pass
    return None

def fetch_and_update():
    print(f"--- Baslatildi: {time.strftime('%H:%M:%S')} ---")
    
    html_content = None
    
    # 1. Yöntem: Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = None
    try:
        print("Selenium baslatiliyor...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.get(NOBET_URL)
        time.sleep(12)
        html_content = driver.page_source
        print(f"Selenium sonucu: {len(html_content) if html_content else 0} karakter.")
    except Exception as e:
        print(f"Selenium hatasi: {e}")
    finally:
        if driver: driver.quit()

    # 2. Yöntem: Eğer Selenium başarısızsa Requests dene
    if not html_content or len(html_content) < 5000:
        html_content = fetch_with_requests()

    if not html_content or len(html_content) < 2000:
        print("HATA: Veri hicbir yontemle alinamadi. Site engelliyor olabilir.")
        return False

    # Sunuculara Gönder
    success_any = False
    for api_url in TARGET_APIS:
        if not api_url or "http" not in api_url: continue
        print(f"Gonderiliyor -> {api_url}")
        try:
            r = requests.post(api_url, json={'html': html_content}, timeout=60)
            print(f"  Yanit: {r.status_code}")
            if r.status_code == 200: success_any = True
        except Exception as e:
            print(f"  Gonderim hatasi: {e}")
    
    return success_any

if __name__ == "__main__":
    success = fetch_and_update()
    # GitHub Action'da her zaman 0 donelim ki diger adimlar (git push gibi) calismaya devam etsin
    sys.exit(0)
