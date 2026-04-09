"""
Nöbetçi Eczane REST API - Render.com Versiyonu
Bu versiyon GitHub Actions ile güncellenen 'page_full.html' dosyasını okur.
"""
import re
import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Yapılandırma
HTML_FILE = "page_full.html"
CACHE_DURATION = 300  # 5 dakika cache (dosya okuma maliyetini azaltmak için)

# Global Cache
cached_data = None
cache_time = None

def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def parse_html(html_content):
    """HTML içeriğini eczane verisine dönüştürür"""
    soup = BeautifulSoup(html_content, "html.parser")
    data = []
    
    h2_list = soup.find_all("h2", class_="vatan_hl")
    
    for h2 in h2_list:
        span = h2.find("span", class_="vatan_span")
        if not span: continue
        
        text = normalize_space(span.get_text())
        parts = text.split()
        if len(parts) < 2: continue
        
        date_str = parts[-1]
        region = " ".join(parts[:-2])
        
        container = h2.parent
        if not container: continue
        
        rows = container.find_all("div", class_="row", style=re.compile(r"margin-bottom"))
        
        for row_div in rows:
            h4 = row_div.find("h4")
            if not h4: continue
            
            pharmacy_name = normalize_space(h4.get_text())
            pharmacy_name = re.sub(r"[›»]", "", pharmacy_name).strip()
            
            until = None
            for strong in row_div.find_all("strong"):
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
                    addr_text = "".join([str(c) if not hasattr(c, 'name') else c.get_text() 
                                       for c in p_tag.contents if c != br_tag])
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
    """Hafızadaki veriyi veya dosyayı döner"""
    global cached_data, cache_time
    
    if cached_data and cache_time:
        if (datetime.now() - cache_time).total_seconds() < CACHE_DURATION:
            return cached_data
            
    try:
        if os.path.exists(HTML_FILE):
            with open(HTML_FILE, 'r', encoding='utf-8') as f:
                html_content = f.read()
            data = parse_html(html_content)
            cached_data = data
            cache_time = datetime.now()
            return data
        return []
    except Exception as e:
        app.logger.error(f"Veri okuma hatası: {e}")
        return cached_data if cached_data else []

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "api": "Nöbetçi Eczane API",
        "platform": "Render.com",
        "endpoints": ["/api/pharmacies", "/api/pharmacies/<region>"]
    })

@app.route('/api/pharmacies', methods=['GET'])
def get_all():
    data = get_pharmacy_data()
    return jsonify({
        "success": True,
        "count": len(data),
        "last_updated": cache_time.isoformat() if cache_time else None,
        "data": data
    })

@app.route('/api/pharmacies/<region>', methods=['GET'])
def get_by_region(region):
    data = get_pharmacy_data()
    region_lower = region.lower()
    filtered = [p for p in data if region_lower in p['region'].lower()]
    return jsonify({
        "success": True,
        "region": region,
        "count": len(filtered),
        "data": filtered
    })

@app.route('/api/update', methods=['POST'])
def update_data():
    """GitHub Actions'tan gelen yeni HTML'i kabul eder"""
    try:
        content = request.json.get('html')
        if not content:
            return jsonify({"success": False, "error": "Boş içerik"}), 400
            
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
            
        global cached_data, cache_time
        cached_data = None
        cache_time = None
        return jsonify({"success": True, "message": "Güncellendi"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Render için port ayarı
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
