import requests
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Hedef API adresleri
RENDER_URL = os.environ.get("RENDER_API_URL", "https://nobet-eczane-api.onrender.com/api/update")
PA_URL = "https://yusuf7007.pythonanywhere.com/api/update"

TARGET_APIS = [RENDER_URL, PA_URL]
NOBET_URL = "https://www.karamaneo.org.tr/nobet-listesi"

def fetch_and_update():
    print("NOBETCI ECZANE Bulut Guncelleyici Baslatildi")
    print(f"Calisma zamani: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Yeni headless modu
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        print(f"Kaynak siteye gidiliyor: {NOBET_URL}")
        # Selenium 4.10+ otomatik driver yönetimi yapar, Service() boş bırakılabilir
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(NOBET_URL)
        
        print("Sayfanin yuklenmesi bekleniyor (15sn)...")
        time.sleep(15)
        
        # Sayfa içeriğini kontrol et
        html_content = driver.page_source
        print(f"Icerik alindi: {len(html_content)} karakter.")
        
        if len(html_content) < 5000:
            print("Hata: Sayfa tam yuklenemedi veya engellendi.")
            return False
            
        success_count = 0
        for api_url in TARGET_APIS:
            if not api_url or "http" not in api_url: continue
            
            print(f"Gonderiliyor: {api_url}")
            try:
                response = requests.post(api_url, json={'html': html_content}, timeout=30)
                if response.status_code == 200:
                    print(f"  BASARILI: {api_url}")
                    success_count += 1
                else:
                    print(f"  Hata ({response.status_code}): {api_url}")
            except Exception as e:
                print(f"  Baglanti Hatasi: {e}")
        
        return success_count > 0
            
    except Exception as e:
        print(f"KRITIK HATA: {str(e)}")
        # Hata anında ekran görüntüsü alamazsak bile hatayı yazdıralım
    finally:
        if driver:
            driver.quit()
    
    return False

if __name__ == "__main__":
    success = fetch_and_update()
    sys.exit(0 if success else 1)
