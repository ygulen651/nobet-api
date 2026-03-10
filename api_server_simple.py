"""
Nöbetçi Eczane REST API - Basitleştirilmiş Versiyon
PythonAnywhere için (Selenium gerektirmez)
"""
import re
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Cache için global değişkenler
cached_data = None
cache_time = None
CACHE_DURATION = 300  # 5 dakika

HTML_FILE = "page_full.html"  # Kaydedilmiş HTML dosyası

def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def parse_html(html_content):
    """HTML içeriğini parse et"""
    soup = BeautifulSoup(html_content, "html.parser")
    data = []
    
    h2_list = soup.find_all("h2", class_="vatan_hl")
    
    for h2 in h2_list:
        span = h2.find("span", class_="vatan_span")
        if not span:
            continue
        
        text = normalize_space(span.get_text())
        parts = text.split()
        if len(parts) < 2:
            continue
        
        date_str = parts[-1]
        region = " ".join(parts[:-2])
        
        container = h2.parent
        if not container:
            continue
        
        rows = container.find_all("div", class_="row", style=re.compile(r"margin-bottom"))
        
        for row_div in rows:
            h4 = row_div.find("h4")
            if not h4:
                continue
            
            pharmacy_name = normalize_space(h4.get_text())
            pharmacy_name = re.sub(r"[›»]", "", pharmacy_name).strip()
            
            until = None
            strong_tags = row_div.find_all("strong")
            for strong in strong_tags:
                strong_text = normalize_space(strong.get_text())
                if "kadar" in strong_text.lower():
                    until = strong_text
                    break
            
            phone = None
            address = None
            p_tag = row_div.find("p")
            if p_tag:
                p_full_text = p_tag.get_text(" ", strip=False)
                
                phone_match = re.search(r'0\d{3}\s*\d{3}\s*\d{2}\s*\d{2}', p_full_text)
                if phone_match:
                    phone = phone_match.group(0).strip()
                
                br_tag = p_tag.find("br")
                if br_tag:
                    addr_text = ""
                    for content in p_tag.contents:
                        if content == br_tag:
                            break
                        if hasattr(content, 'get_text'):
                            addr_text += content.get_text()
                        elif not hasattr(content, 'name'):
                            addr_text += str(content)
                    
                    address = normalize_space(addr_text)
                    address = re.sub(r'[\ue802-\ue850]', '', address).strip()
            
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

def get_pharmacy_data():
    """HTML dosyasından veriyi çek"""
    global cached_data, cache_time
    
    # Cache kontrolü
    if cached_data and cache_time:
        elapsed = (datetime.now() - cache_time).total_seconds()
        if elapsed < CACHE_DURATION:
            return cached_data
    
    # HTML dosyasını oku
    try:
        if os.path.exists(HTML_FILE):
            with open(HTML_FILE, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            data = parse_html(html_content)
            cached_data = data
            cache_time = datetime.now()
            return data
        else:
            return []
    except Exception as e:
        print(f"Hata: {e}")
        return cached_data if cached_data else []

@app.route('/')
def home():
    """API ana sayfa"""
    return jsonify({
        "api": "Nöbetçi Eczane API",
        "version": "1.0 (Basit)",
        "endpoints": {
            "/api/pharmacies": "Tüm nöbetçi eczaneler",
            "/api/pharmacies/<region>": "Belirli bölgenin eczaneleri",
            "/api/refresh": "Cache'i temizle ve yeniden yükle",
            "/api/update": "HTML dosyasını güncelle (POST)"
        },
        "note": "HTML dosyasından veri okuyor (page_full.html)"
    })

@app.route('/api/pharmacies', methods=['GET'])
def get_all_pharmacies():
    """Tüm nöbetçi eczaneleri getir"""
    try:
        data = get_pharmacy_data()
        
        return jsonify({
            "success": True,
            "count": len(data),
            "cached": cache_time.isoformat() if cache_time else None,
            "source": "page_full.html",
            "data": data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/pharmacies/<region>', methods=['GET'])
def get_pharmacies_by_region(region):
    """Belirli bölgenin eczanelerini getir"""
    try:
        data = get_pharmacy_data()
        
        region_lower = region.lower()
        filtered = [p for p in data if region_lower in p['region'].lower()]
        
        return jsonify({
            "success": True,
            "region": region,
            "count": len(filtered),
            "data": filtered
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/refresh', methods=['POST'])
def refresh_cache():
    """Cache'i temizle ve yeniden yükle"""
    global cached_data, cache_time
    cached_data = None
    cache_time = None
    
    data = get_pharmacy_data()
    
    return jsonify({
        "success": True,
        "message": "Cache yenilendi",
        "count": len(data)
    })

@app.route('/api/update', methods=['POST'])
def update_html():
    """HTML dosyasını güncelle (yeni veri için)"""
    try:
        if 'html' not in request.json:
            return jsonify({"success": False, "error": "HTML verisi gerekli"}), 400
        
        html_content = request.json['html']
        
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Cache'i temizle
        global cached_data, cache_time
        cached_data = None
        cache_time = None
        
        return jsonify({
            "success": True,
            "message": "HTML dosyası güncellendi"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Nöbetçi Eczane API (Basit Versiyon)")
    print("=" * 50)
    print(f"\nHTML Dosyası: {HTML_FILE}")
    print(f"Dosya var mı: {os.path.exists(HTML_FILE)}")
    print("\nEndpoint'ler:")
    print("  - http://localhost:5000/api/pharmacies")
    print("  - http://localhost:5000/api/pharmacies/merkez")
    print("  - http://localhost:5000/api/refresh (POST)")
    print("  - http://localhost:5000/api/update (POST)")
    print("\n" + "=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)







