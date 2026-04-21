import requests
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Yapılandırma
TARGET_APIS = [
    "https://nobet-eczane-api.onrender.com/api/update",
    "https://yusuf7007.pythonanywhere.com/api/update"
]
LOCAL_HTML_FILE = "page_full.html"
NOBET_URL = "https://www.karamaneo.org.tr/nobet-listesi"

def fetch_fresh_html():
    """Web sitesinden yeni HTML çek (Selenium kullanarak)"""
    print(f"Kaynaksiteye gidiliyor: {NOBET_URL}")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(NOBET_URL)
        
        print("Sayfanin yuklenmesi bekleniyor...")
        time.sleep(5)
        
        try:
            # Veri yapısının geldiğinden emin ol
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vatan_hl"))
            )
            print("Veri yapisi dogrulandi.")
        except Exception as e:
            print(f"Uyari: vatan_hl sinifi bulunamadi, yine de icerik aliniyor... ({e})")
        
        html_content = driver.page_source
        driver.quit()
        
        if len(html_content) < 5000:
            print(f"Hata: Alinan HTML cok kisa ({len(html_content)} karakter). Bot korumasina takilmis olabilir.")
            return None
            
        print(f"Icerik basariyla alindi ({len(html_content)} karakter).")
        return html_content
    except Exception as e:
        print(f"Tarayici Hatasi: {str(e)}")
        return None

def update_local_file(html_content):
    """Yerel dosyayı günceller"""
    try:
        with open(LOCAL_HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Yerel dosya guncellendi: {LOCAL_HTML_FILE}")
        return True
    except Exception as e:
        print(f"Yerel dosya yazma hatasi: {e}")
        return False

def update_remote_apis(html_content):
    """Bulut sunucularını günceller"""
    success_count = 0
    for api_url in TARGET_APIS:
        print(f"API guncelleniyor: {api_url}")
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
                    print(f"  API Hatasi: {result.get('error')}")
            else:
                print(f"  HTTP Hatasi: {response.status_code}")
        except Exception as e:
            print(f"  Iletisim Hatasi: {e}")
    
    return success_count

def main():
    print("=" * 60)
    print("   NOBETCI ECZANE - TAM SINKRONIZASYON SISTEMI")
    print("=" * 60)
    
    # 1. Veriyi çek
    html = fetch_fresh_html()
    if not html:
        print("\nVeri alinamadigi icin islem durduruldu.")
        sys.exit(1)
        
    # 2. Yerel dosyayı güncelle
    update_local_file(html)
    
    # 3. Uzak sunucuları güncelle
    print("\nBulut sunuculari guncelleniyor...")
    count = update_remote_apis(html)
    
    print("\n" + "=" * 60)
    if count > 0:
        print(f"ISLEM TAMAMLANDI! {count} bulut sunucusu guncellendi.")
    else:
        print("Yerel dosya guncellendi ama bulut sunucularina ulasilamadi.")
    print("=" * 60)

if __name__ == "__main__":
    main()
