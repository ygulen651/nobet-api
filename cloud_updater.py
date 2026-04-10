import requests
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Hedef API adresleri
# Render URL'sini hem ortam değişkeninden alıyoruz hem de varsayılan olarak ekliyoruz
RENDER_URL = os.environ.get("RENDER_API_URL", "https://nobet-eczane-api.onrender.com/api/update")
PA_URL = "https://yusuf7007.pythonanywhere.com/api/update"

TARGET_APIS = [RENDER_URL, PA_URL]

NOBET_URL = "https://www.karamaneo.org.tr/nobet-listesi"

def fetch_and_update():
    print("NOBETCI ECZANE Bulut Guncelleyici Baslatildi")
    print(f"Calisma zamani: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # User agent ekleyerek bot korumasini gecmeye calisalim
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        print(f"Kaynak siteye gidiliyor: {NOBET_URL}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(NOBET_URL)
        
        # Sayfanin yuklenmesini bekle
        print("Bekleniyor (10sn)...")
        time.sleep(10)
        
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vatan_hl"))
            )
            print("Veri yapisi (vatan_hl) bulundu.")
        except Exception as e:
            print(f"Uyari: Veri yapisi tam dogrulanamadi, yine de devam ediliyor... ({e})")
        
        html_content = driver.page_source
        
        if len(html_content) < 5000:
            print(f"Hata: Alinan HTML cok kisa ({len(html_content)} karakter). Engellenmis olabilir.")
            # Sayfa basligini kontrol et
            print(f"Sayfa Basligi: {driver.title}")
            return False
            
        print(f"Icerik basariyla alindi ({len(html_content)} karakter). Bulut sunucularina gonderiliyor...")
        
        success_count = 0
        for api_url in TARGET_APIS:
            if not api_url or "api/update" not in api_url: continue
            
            print(f"Gonderiliyor: {api_url}")
            try:
                response = requests.post(
                    api_url,
                    json={'html': html_content},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"  BASARILI: {api_url} guncellendi!")
                        success_count += 1
                    else:
                        print(f"  API Hatasi ({api_url}): {result.get('error')}")
                else:
                    print(f"  HTTP Hatasi ({api_url}): {response.status_code}")
            except Exception as e:
                print(f"  Iletisim Hatasi ({api_url}): {e}")
        
        return success_count > 0
            
    except Exception as e:
        print(f"KRITIK HATA: {str(e)}")
    finally:
        if driver:
            driver.quit()
    
    return False

if __name__ == "__main__":
    success = fetch_and_update()
    if not success:
        print("Guncelleme basarisiz oldu.")
        sys.exit(1)
    else:
        print("Tum islemler basariyla tamamlandi.")
        sys.exit(0)
