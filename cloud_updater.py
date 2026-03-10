import requests
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PYTHONANYWHERE_API = "https://yusuf7007.pythonanywhere.com/api/update"
NOBET_URL = "https://www.karamaneo.org.tr/nobet-listesi"

def fetch_and_update():
    print("🚀 Nöbetçi Eczane Bulut Güncelleyici Başlatıldı")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # GitHub Actions'ta Chrome genellikle yüklüdür
        driver = webdriver.Chrome(options=chrome_options)
        print(f"🔗 Sayfaya gidiliyor: {NOBET_URL}")
        driver.get(NOBET_URL)
        
        # Sayfanın yüklenmesini bekle
        time.sleep(5)
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vatan_hl"))
            )
            print("✅ Veri yapısı bulundu.")
        except Exception as e:
            print(f"⚠️ Uyarı: vatan_hl sınıfı hemen bulunamadı, devam ediliyor... ({e})")
        
        html_content = driver.page_source
        driver.quit()
        
        if len(html_content) < 5000:
            print(f"❌ Hata: Alınan HTML çok kısa ({len(html_content)} karakter). Bot korumasına takılmış olabilir.")
            return False
            
        print(f"📦 HTML alındı ({len(html_content)} karakter). PythonAnywhere'e gönderiliyor...")
        
        response = requests.post(
            PYTHONANYWHERE_API,
            json={'html': html_content},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("🎉 BAŞARILI: PythonAnywhere güncellendi!")
                return True
            else:
                print(f"❌ API Hatası: {result.get('error')}")
        else:
            print(f"❌ HTTP Hatası: {response.status_code}")
            
    except Exception as e:
        print(f"💥 KRİTİK HATA: {str(e)}")
    
    return False

if __name__ == "__main__":
    fetch_and_update()
