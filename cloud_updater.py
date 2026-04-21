import requests
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# API Adresleri
# GitHub Secrets'tan RENDER_API_URL yoksa varsayılanı kullan
RENDER_URL = os.environ.get("RENDER_API_URL", "https://nobet-eczane-api.onrender.com/api/update")
PA_URL = "https://yusuf7007.pythonanywhere.com/api/update"

TARGET_APIS = [RENDER_URL, PA_URL]
NOBET_URL = "https://www.karamaneo.org.tr/nobet-listesi"

def fetch_and_update():
    print(f"--- Guncelleme Baslatildi: {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        print(f"Kaynak siteye gidiliyor: {NOBET_URL}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.get(NOBET_URL)
        
        # Sayfanın tam yüklenmesi için bekle
        time.sleep(10)
        
        html_content = driver.page_source
        content_len = len(html_content)
        print(f"Icerik alindi: {content_len} karakter.")
        
        if content_len < 1000:
            print("Hata: Icerik cok kisa, muhtemelen engellendi.")
            return False
            
        # Sunucuları güncelle
        success_any = False
        for api_url in TARGET_APIS:
            if not api_url or "http" not in api_url: continue
            
            print(f"Gonderiliyor: {api_url}")
            try:
                # 60 saniye timeout - Render bazen geç uyanır
                r = requests.post(api_url, json={'html': html_content}, timeout=60)
                if r.status_code == 200:
                    print(f"  OK: {api_url}")
                    success_any = True
                else:
                    print(f"  Hata ({r.status_code}): {api_url}")
            except Exception as e:
                print(f"  Baglanti Hatasi ({api_url}): {e}")
        
        return success_any
            
    except Exception as e:
        print(f"KRITIK HATA: {e}")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # GitHub Action'ın hata vermemesi için başarılı bir işlem yapıldıysa 0 dön
    success = fetch_and_update()
    sys.exit(0 if success else 1)
