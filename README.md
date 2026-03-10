# Nöbetçi Eczane Listesi Scraper

Karaman Eczacı Odası web sitesinden nöbetçi eczane listesini çeken Python scripti.

## Kurulum

```bash
pip install -r requirements.txt
```

**Not:** Selenium kullanmak için Chrome tarayıcısı ve ChromeDriver kurulu olmalı.

## Kullanım

### Yöntem 1: Selenium ile (Önerilen)

Web sitesini gerçek bir tarayıcı gibi ziyaret eder, JavaScript içeriğini çalıştırır:

```bash
python nobet_scraper_selenium.py
```

Menüden `1` seçin.

### Yöntem 2: Kaydedilmiş HTML'den Okuma

Eğer web sitesine erişim sorunu varsa veya hızlı test için:

```bash
python nobet_scraper_selenium.py
```

Menüden `2` seçin (page_full.html dosyasını kullanır).

### Yöntem 3: Basit Requests (Çalışmıyor)

```bash
python nobet_scraper.py
```

**Uyarı:** Web sitesi bot koruması kullandığı için bu yöntem şu anda çalışmıyor.

## Sorun Giderme

### Web Sitesi Bot Koruması

Web sitesi bot tespit sistemi kullanıyor ve basit HTTP isteklerine kısıtlı içerik döndürüyor. Bu yüzden:

- **Selenium kullanın** (tarayıcı gibi davranır)
- Ya da tarayıcıdan sayfayı manuel kaydedin ve `page_full.html` olarak kaydedin

### ChromeDriver Kurulumu

ChromeDriver'ı otomatik yönetmek için:

```bash
pip install webdriver-manager
```

Sonra `nobet_scraper_selenium.py` içinde:

```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
```

## Çıktı Formatı

Script JSON formatında veri döndürür:

```json
[
  {
    "region": "Merkez Nöbetçi",
    "date": "15-12-2025",
    "name": "ARSLANTAS",
    "until": "16/12/2025 08:00'e kadar",
    "phone": "0338 212 94 94",
    "address": "Yeni Devlet Hastanesi Karşısı...",
    "map": "https://maps.google.com/?ll=37.166026,33.254976..."
  }
]
```

## Dosyalar

- `nobet_scraper.py` - Basit requests versiyonu (şu anda çalışmıyor)
- `nobet_scraper_selenium.py` - Selenium versiyonu (önerilen)
- `api_server.py` - 🆕 REST API (mobil entegrasyon için)
- `MOBIL_ENTEGRASYON.md` - 📱 Mobil uygulama entegrasyon kılavuzu
- `page_full.html` - Test için kaydedilmiş HTML
- `requirements.txt` - Python bağımlılıkları

## 📱 Mobil Uygulama Entegrasyonu

API sunucusunu başlatın:

```bash
python api_server.py
```

Endpoint'ler:
- `GET /api/pharmacies` - Tüm eczaneler
- `GET /api/pharmacies/{region}` - Bölgeye göre filtre
- `POST /api/refresh` - Cache'i yenile

Detaylı bilgi için `MOBIL_ENTEGRASYON.md` dosyasına bakın.

## Lisans

Bu script sadece eğitim amaçlıdır.

