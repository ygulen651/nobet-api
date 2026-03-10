"""
Nöbetçi Eczane - Arka Plan Otomatik Güncelleme Servisi
Bu script arka planda çalışır ve her 6 saatte bir verileri günceller.
"""
import time
import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# AYARLAR
PYTHONANYWHERE_API = "https://yusuf7007.pythonanywhere.com/api/update"
NOBET_URL = "https://www.karamaneo.org.tr/nobet-listesi"
GUNCELLEME_ARALIGI = 6 * 60 * 60  # 6 saat (saniye cinsinden)

def log(mesaj):
    zaman = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"[{zaman}] {mesaj}")
    # İsteğe bağlı dosyaya da yazılabilir:
    with open("guncelleme_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{zaman}] {mesaj}\n")

def fetch_and_update():
    log("Güncelleme işlemi başlatılıyor...")
    
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
        
        if not html_content or len(html_content) < 1000:
            log("❌ Hata: Web sitesinden geçerli veri alınamadı.")
            return False
            
        log(f"✅ HTML alındı ({len(html_content)} karakter). PythonAnywhere'e gönderiliyor...")
        
        response = requests.post(
            PYTHONANYWHERE_API,
            json={'html': html_content},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                log("🎉 BAŞARILI: PythonAnywhere güncellendi!")
                return True
            else:
                log(f"❌ API Hatası: {data.get('error')}")
        else:
            log(f"❌ HTTP Hatası: {response.status_code}")
            
    except Exception as e:
        log(f"❌ BEKLENMEDİK HATA: {str(e)}")
    
    return False

def main():
    log("Otomatik Güncelleme Servisi Başlatıldı (Her 6 saatte bir çalışacak)")
    
    while True:
        success = fetch_and_update()
        
        if success:
            log(f"Bekleme moduna geçiliyor... (Sonraki güncelleme 6 saat sonra)")
            time.sleep(GUNCELLEME_ARALIGI)
        else:
            log("İşlem başarısız oldu. 10 dakika sonra tekrar denenecek...")
            time.sleep(10 * 60) # Hata durumunda 10 dk bekle

if __name__ == "__main__":
    main()
