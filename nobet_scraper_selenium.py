import re
import json
import time
from bs4 import BeautifulSoup

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Selenium kurulu değil. Kurmak için: pip install selenium")

URL = "https://www.karamaneo.org.tr/nobet-listesi"

def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def fetch_nobet_list_selenium():
    """Selenium kullanarak sayfa içeriğini çek"""
    if not SELENIUM_AVAILABLE:
        print("Selenium kurulu değil!")
        return []
    
    # Chrome seçenekleri
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı gösterme
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        print("Tarayıcı başlatılıyor...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"Sayfa yükleniyor: {URL}")
        driver.get(URL)
        
        # Sayfanın yüklenmesini bekle
        time.sleep(3)
        
        # H2 etiketlerinin yüklenmesini bekle
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vatan_hl"))
            )
        except:
            print("Sayfa elementleri yüklenemedi!")
        
        # Sayfayı kaydet
        html_content = driver.page_source
        print(f"Sayfa içeriği alındı: {len(html_content)} karakter")
        
        # HTML'i kaydet
        with open("selenium_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("HTML 'selenium_page.html' dosyasına kaydedildi.")
        
        driver.quit()
        
        return parse_html(html_content)
        
    except Exception as e:
        print(f"Selenium hatası: {e}")
        return []

def parse_html(html_content):
    """HTML içeriğini parse et ve eczane bilgilerini çıkar"""
    soup = BeautifulSoup(html_content, "html.parser")
    data = []

    # H2 etiketlerini bul
    h2_list = soup.find_all("h2", class_="vatan_hl")
    
    if not h2_list:
        print("H2 etiketi bulunamadı!")
        return []
    
    print(f"{len(h2_list)} bölge bulundu.")
    
    for h2 in h2_list:
        span = h2.find("span", class_="vatan_span")
        if not span:
            continue
        
        # Bölge ve tarihi ayır
        text = normalize_space(span.get_text())
        parts = text.split()
        if len(parts) < 2:
            continue
        
        date_str = parts[-1]
        region = " ".join(parts[:-2])
        
        # H2'nin parent container'ını al
        container = h2.parent
        if not container:
            continue
        
        # Container içindeki div.row'ları bul
        rows = container.find_all("div", class_="row", style=re.compile(r"margin-bottom"))
        
        for row_div in rows:
            h4 = row_div.find("h4")
            if not h4:
                continue
            
            # Eczane adı
            pharmacy_name = normalize_space(h4.get_text())
            pharmacy_name = re.sub(r"[›»]", "", pharmacy_name).strip()
            
            # Süre bilgisi
            until = None
            strong_tags = row_div.find_all("strong")
            for strong in strong_tags:
                strong_text = normalize_space(strong.get_text())
                if "kadar" in strong_text.lower():
                    until = strong_text
                    break
            
            # Telefon ve adres - p tag içeriğinden çıkar
            phone = None
            address = None
            p_tag = row_div.find("p")
            if p_tag:
                # P tag'inin text içeriğini al
                p_full_text = p_tag.get_text(" ", strip=False)
                
                # Telefon numarası: Türkiye formatı (0xxx xxx xx xx veya benzer)
                phone_match = re.search(r'0\d{3}\s*\d{3}\s*\d{2}\s*\d{2}', p_full_text)
                if phone_match:
                    phone = phone_match.group(0).strip()
                
                # Adres: İlk br'ye kadar olan kısım (telefon hariç)
                # P içindeki text'i br ile böl
                br_tag = p_tag.find("br")
                if br_tag:
                    # br'den önceki kısmı al
                    addr_text = ""
                    for content in p_tag.contents:
                        if content == br_tag:
                            break
                        if hasattr(content, 'get_text'):
                            addr_text += content.get_text()
                        elif not hasattr(content, 'name'):  # String
                            addr_text += str(content)
                    
                    # Adres temizliği
                    address = normalize_space(addr_text)
                    # İkonları temizle
                    address = re.sub(r'[\ue802-\ue850]', '', address).strip()
            
            # Harita linki
            map_url = None
            map_link = row_div.find("a", href=re.compile(r"maps\.google"))
            if map_link:
                map_url = map_link.get("href")
            
            data.append({
                "region": region,
                "date": date_str,
                "name": pharmacy_name,
                "until": until,
                "phone": phone,
                "address": address,
                "map": map_url
            })
    
    return data

def fetch_from_file(filename="page_full.html"):
    """Kaydedilmiş HTML dosyasından veri çek"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            html_content = f.read()
        print(f"'{filename}' dosyasından okunuyor...")
        return parse_html(html_content)
    except FileNotFoundError:
        print(f"'{filename}' dosyası bulunamadı!")
        return []

if __name__ == "__main__":
    print("=== Nöbetçi Eczane Listesi ===\n")
    print("1. Selenium ile web sitesinden çek (önerilen)")
    print("2. Kaydedilmiş HTML dosyasından oku (page_full.html)")
    print()
    
    choice = input("Seçiminiz (1/2): ").strip()
    
    if choice == "1":
        result = fetch_nobet_list_selenium()
    elif choice == "2":
        result = fetch_from_file()
    else:
        print("Geçersiz seçim! Kaydedilmiş dosyadan okumaya devam ediliyor...")
        result = fetch_from_file()
    
    print("\n" + "="*50)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nToplam {len(result)} nöbetçi eczane bulundu.")

