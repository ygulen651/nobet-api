"""
PythonAnywhere'deki HTML'i Otomatik Güncelle
Haftalık çalıştır (Windows Görev Zamanlayıcı ile)
"""
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# PythonAnywhere API bilgileri
PYTHONANYWHERE_API = "https://yusuf7007.pythonanywhere.com/api/update"
NOBET_URL = "https://www.karamaneo.org.tr/nobet-listesi"

def fetch_fresh_html():
    """Web sitesinden yeni HTML çek"""
    print("Web sitesinden yeni veri çekiliyor...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(NOBET_URL)
        time.sleep(3)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vatan_hl"))
            )
        except:
            pass
        
        html_content = driver.page_source
        driver.quit()
        
        print(f"✅ HTML alındı: {len(html_content)} karakter")
        return html_content
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def update_pythonanywhere(html_content):
    """PythonAnywhere'e yeni HTML'i gönder"""
    print("PythonAnywhere güncelleniyor...")
    
    try:
        response = requests.post(
            PYTHONANYWHERE_API,
            json={'html': html_content},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ PythonAnywhere güncellendi!")
                return True
            else:
                print(f"❌ API hatası: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP hatası: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def main():
    print("=" * 50)
    print("Nöbetçi Eczane - Otomatik Güncelleme")
    print("=" * 50)
    print()
    
    # 1. Yeni HTML çek
    html = fetch_fresh_html()
    if not html:
        print("❌ HTML alınamadı, işlem iptal edildi.")
        return
    
    # 2. PythonAnywhere'e gönder
    success = update_pythonanywhere(html)
    
    if success:
        print()
        print("=" * 50)
        print("🎉 Güncelleme başarılı!")
        print("API: https://yusuf7007.pythonanywhere.com/api/pharmacies")
        print("=" * 50)
    else:
        print()
        print("=" * 50)
        print("⚠️ Güncelleme başarısız!")
        print("=" * 50)

if __name__ == "__main__":
    main()

