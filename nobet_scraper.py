import re
import json
import time
import requests
from bs4 import BeautifulSoup

URL = "https://www.karamaneo.org.tr/nobet-listesi"

def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def fetch_nobet_list():
    # Session kullan - cookieleri saklar
    session = requests.Session()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    
    # Önce ana sayfaya git (cookie almak için)
    try:
        session.get("https://www.karamaneo.org.tr/", timeout=10, headers=headers)
        time.sleep(1)
    except:
        pass
    
    # Yeniden deneme mekanizması
    max_retries = 3
    html_content = None
    
    for attempt in range(max_retries):
        try:
            r = session.get(URL, timeout=20, headers=headers, verify=True)
            r.raise_for_status()
            html_content = r.text
            
            # İçeriğin yeterli uzunlukta olduğunu kontrol et
            if len(html_content) > 10000:  # En az 10KB olmalı
                break
            else:
                print(f"İçerik çok kısa ({len(html_content)} karakter), yeniden deneniyor...")
                time.sleep(2)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < max_retries - 1:
                print(f"Bağlantı hatası, {attempt + 1}. deneme başarısız. Yeniden deneniyor...")
                time.sleep(2)
            else:
                print(f"Bağlantı kurulamadı: {e}")
                return []
    
    if not html_content or len(html_content) < 1000:
        print(f"Yetersiz içerik alındı: {len(html_content) if html_content else 0} karakter")
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    data = []

    # H2 etiketlerini bul ve onların parent container'larını kullan
    h2_list = soup.find_all("h2", class_="vatan_hl")
    
    if not h2_list:
        print("H2 etiketi bulunamadı. Web sitesi farklı içerik dönüyor olabilir.")
        return []
    
    for h2 in h2_list:
        span = h2.find("span", class_="vatan_span")
        if not span:
            continue
        
        # Bölge ve tarihi ayır
        text = normalize_space(span.get_text())
        # "Merkez Nöbetçi Eczaneler 15-12-2025" formatında
        parts = text.split()
        if len(parts) < 2:
            continue
        
        # Son kısım tarih olmalı
        date_str = parts[-1]
        # "Nöbetçi Eczaneler" kısmını çıkar
        region = " ".join(parts[:-2])
        
        # H2'nin parent container'ını al
        container = h2.parent
        if not container:
            continue
        
        # Bu container içindeki tüm div.row'ları bul (margin-bottom style'ı olanlar eczane bilgisi içerir)
        rows = container.find_all("div", class_="row", style=re.compile(r"margin-bottom"))
        
        for row_div in rows:
            # H4 etiketini bul
            h4 = row_div.find("h4")
            if not h4:
                continue
            
            # Eczane adını al
            pharmacy_name = normalize_space(h4.get_text())
            # Icon varsa temizle
            pharmacy_name = re.sub(r"[›»]", "", pharmacy_name).strip()
            
            # Süre bilgisini bul
            until = None
            strong_tags = row_div.find_all("strong")
            for strong in strong_tags:
                strong_text = normalize_space(strong.get_text())
                if "kadar" in strong_text.lower():
                    until = strong_text
                    break
            
            # Paragraf içinden telefon ve adres bilgilerini çıkar
            phone = None
            address = None
            p_tag = row_div.find("p")
            if p_tag:
                # Adres: icon-home ile br arası
                home_icon = p_tag.find("i", class_="icon-home")
                if home_icon:
                    addr_parts = []
                    for sibling in home_icon.next_siblings:
                        if hasattr(sibling, 'name'):
                            if sibling.name == 'br':
                                break
                        else:
                            addr_parts.append(str(sibling))
                    address = normalize_space("".join(addr_parts))
                
                # Telefon: icon-phone sonrası, "-" işaretine kadar
                phone_icon = p_tag.find("i", class_="icon-phone")
                if phone_icon:
                    phone_parts = []
                    for sibling in phone_icon.next_siblings:
                        text_content = str(sibling).strip()
                        if hasattr(sibling, 'name'):
                            break
                        if text_content and text_content != "-":
                            phone_parts.append(text_content)
                        if "-" in text_content:
                            break
                    phone = normalize_space("".join(phone_parts).replace("-", "").strip())
            
            # Harita linkini bul
            map_url = None
            map_link = row_div.find("a", href=re.compile(r"maps\.google"))
            if map_link:
                map_url = map_link.get("href")
            
            # Veriyi ekle
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

if __name__ == "__main__":
    result = fetch_nobet_list()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nToplam {len(result)} nöbetçi eczane bulundu.")
