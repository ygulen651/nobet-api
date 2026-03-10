# 🚀 API Deployment Rehberi

## 🎯 Hızlı Karşılaştırma

| Yöntem | Maliyet | Süre | 7/24 | Zorluk |
|--------|---------|------|------|--------|
| **Render.com** | ✅ Ücretsiz | 10 dk | ✅ Evet | ⭐⭐ |
| **PythonAnywhere** | ✅ Ücretsiz | 5 dk | ✅ Evet | ⭐ |
| **Ngrok** | ✅ Ücretsiz | 2 dk | ❌ Hayır | ⭐ |
| **Lokal (Arka Plan)** | ✅ Ücretsiz | 1 dk | ⚠️ PC açıkken | ⭐ |

---

## 1️⃣ Render.com (ÖNERİLEN) ⭐

### Avantajlar
- ✅ Tamamen ücretsiz
- ✅ Otomatik SSL (HTTPS)
- ✅ 7/24 çalışır
- ✅ GitHub entegrasyonu
- ✅ Otomatik restart

### Adımlar

#### 1. GitHub'a Yükle

```bash
# Git yok ise kur: https://git-scm.com/

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADIN/nobet-api.git
git push -u origin main
```

#### 2. Render.com'a Kayıt Ol

- render.com adresine git
- GitHub ile giriş yap

#### 3. Yeni Web Service Oluştur

- "New +" → "Web Service"
- GitHub repo'nu seç
- Ayarlar:
  - **Name:** nobet-eczane-api
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `python api_server.py`
  - **Plan:** Free

#### 4. Deploy Et

- "Create Web Service" tıkla
- 5-10 dakika bekle

#### 5. Kullan

API adresi: `https://nobet-eczane-api.onrender.com`

Mobil uygulamanda:
```kotlin
const val API_BASE = "https://nobet-eczane-api.onrender.com"
```

---

## 2️⃣ PythonAnywhere (EN KOLAY) 🐍

### Adımlar

#### 1. Hesap Oluştur
- pythonanywhere.com
- "Start running Python online" → Sign up
- Beginner (ücretsiz) seç

#### 2. Dosyaları Yükle

- Files → Upload
- Tüm dosyaları yükle:
  - `api_server.py`
  - `requirements.txt`
  - `nobet_scraper_selenium.py`

#### 3. Web App Oluştur

- Web → Add a new web app
- Flask seç
- Python 3.10 seç

#### 4. WSGI Dosyasını Düzenle

`/var/www/kullaniciadin_pythonanywhere_com_wsgi.py`:

```python
import sys
path = '/home/kullaniciadin'
if path not in sys.path:
    sys.path.append(path)

from api_server import app as application
```

#### 5. Requirements Kur

- Consoles → Bash
```bash
pip install --user -r requirements.txt
```

#### 6. Reload

- Web → Reload button

#### 7. Kullan

API adresi: `https://kullaniciadin.pythonanywhere.com`

---

## 3️⃣ Ngrok (GELİŞTİRME İÇİN) 🔗

Lokal API'ni internete aç (geçici, test için).

### Kurulum

1. ngrok.com'dan indir
2. Kayıt ol, auth token al

```bash
ngrok config add-authtoken YOUR_TOKEN
```

### Kullanım

```bash
# Terminal 1: API'yi başlat
python api_server.py

# Terminal 2: Ngrok başlat
ngrok http 5000
```

**Çıktı:**
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
```

Mobil uygulamada: `https://abc123.ngrok.io`

⚠️ **Dikkat:** Her başlattığında URL değişir, kalıcı değil!

---

## 4️⃣ Lokal (Arka Plan) 💻

### Windows

`start_api.bat` dosyasını çift tıkla:

```batch
@echo off
start /B pythonw api_server.py
```

### macOS/Linux

```bash
nohup python api_server.py > api.log 2>&1 &
```

Durdurmak için:
```bash
# PID bul
ps aux | grep api_server.py

# Durdur
kill -9 PID
```

### Otomatik Başlatma (Windows)

1. `start_api.bat` oluştur
2. `Win + R` → `shell:startup`
3. Batch dosyasının kısayolunu buraya koy
4. Bilgisayar açılınca otomatik başlar

---

## 5️⃣ Heroku (ÜCRETLİ) 💰

Artık ücretsiz plan yok, aylık $7.

### Adımlar

```bash
# Heroku CLI kur
heroku login

# Procfile oluştur
echo "web: python api_server.py" > Procfile

# Deploy
heroku create nobet-api
git push heroku main
```

---

## 🔒 Güvenlik (Production için)

### API Key Ekle

`api_server.py` güncellemesi:

```python
import os
from functools import wraps

API_KEY = os.environ.get('API_KEY', 'default-secret-key')

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key and key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    return decorated

@app.route('/api/pharmacies')
@require_api_key
def get_all_pharmacies():
    # ...
```

Mobil uygulamadan:
```kotlin
request.addHeader("X-API-Key", "your-secret-key")
```

---

## 📊 İzleme

### Logs İzle

**Render:**
- Dashboard → Logs sekmesi

**PythonAnywhere:**
- Web → Log files

**Lokal:**
```bash
tail -f api.log
```

---

## 🎯 Tavsiyem

**Başlangıç:** Render.com (ücretsiz, kolay, güvenilir)
**Geliştirme:** Ngrok (hızlı test)
**Production:** Render.com veya kendi sunucu

---

## 🆘 Sorun Giderme

### API Başlamıyor

```bash
# Port kullanımda mı kontrol et
netstat -ano | findstr :5000

# Port değiştir
python api_server.py --port 8000
```

### Selenium Hatası

Production'da Selenium yerine cache kullan:
- Lokal'de veri çek
- JSON'a kaydet
- Sunucudan JSON'u sun

### CORS Hatası

Mobil uygulamadan istek atarken CORS hatası alıyorsan, zaten `flask-cors` kurulu, sorun yok.

---

## 📞 İletişim

Sorun mu var? `MOBIL_ENTEGRASYON.md` dosyasına bak.







