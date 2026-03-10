# 🚀 PythonAnywhere Kurulum Rehberi (5 Dakika)

## ✨ Neden PythonAnywhere?

- ✅ EN KOLAY yöntem
- ✅ GitHub gerekmez
- ✅ Tamamen ücretsiz
- ✅ 7/24 çalışır
- ✅ Selenium gerektirmez (basit versiyon)

---

## 📋 Adım Adım Kurulum

### 1️⃣ Hesap Aç (2 dakika)

1. **https://www.pythonanywhere.com** adresine git
2. **"Pricing & signup"** butonuna tıkla
3. **"Create a Beginner account"** (ücretsiz) seç
4. Email, kullanıcı adı, şifre belirle
5. Email'ini doğrula

✅ Hesap hazır!

---

### 2️⃣ Dosyaları Yükle (1 dakika)

Dashboard'da **"Files"** sekmesine git.

**Şu 3 dosyayı yükle:**

1. ✅ `api_server_simple.py` (basit versiyon - Selenium yok)
2. ✅ `page_full.html` (veri dosyası)
3. ✅ `requirements.txt`

> **Not:** `api_server.py` DEĞİL, `api_server_simple.py` yükle!

---

### 3️⃣ Kütüphaneleri Kur (1 dakika)

1. **"Consoles"** sekmesi → **"Bash"** tıkla
2. Aşağıdaki komutu çalıştır:

```bash
pip3 install --user flask flask-cors beautifulsoup4 requests
```

✅ "Successfully installed" yazısını bekle (30 saniye)

---

### 4️⃣ Web App Oluştur (1 dakika)

1. **"Web"** sekmesine git
2. **"Add a new web app"** butonuna tıkla
3. Domain adını kabul et → **"Next"**
4. Framework olarak **"Flask"** seç
5. Python versiyonu **"3.10"** seç
6. **"Next"** → **"Next"**

---

### 5️⃣ WSGI Dosyasını Düzenle (30 saniye)

**"Web"** sekmesinde:

1. **"WSGI configuration file"** linkine tıkla
2. Tüm içeriği sil
3. Aşağıdaki kodu yapıştır:

```python
import sys
import os

# Dosya yolunu ekle (KULLANICI_ADIN yerine senin kullanıcı adını yaz!)
path = '/home/KULLANICI_ADIN'
if path not in sys.path:
    sys.path.append(path)

# API'yi yükle
from api_server_simple import app as application
```

> **ÖNEMLİ:** `KULLANICI_ADIN` yerine kendi kullanıcı adını yaz!
> Örnek: `/home/ahmet` veya `/home/mehmet123`

4. **"Save"** butonuna bas (sağ üstte)

---

### 6️⃣ Başlat! (10 saniye)

1. **"Web"** sekmesine geri dön
2. Yeşil **"Reload kullaniciadin.pythonanywhere.com"** butonuna tıkla

⏳ 5 saniye bekle...

---

### 7️⃣ Test Et! (20 saniye)

Tarayıcında aç:

```
https://KULLANICI_ADIN.pythonanywhere.com/api/pharmacies
```

✅ JSON veri göreceksin! 🎉

---

## 📱 Mobil Uygulamada Kullan

### Android (Kotlin)

```kotlin
object ApiConfig {
    const val BASE_URL = "https://KULLANICI_ADIN.pythonanywhere.com/"
}

// Retrofit
interface PharmacyApi {
    @GET("api/pharmacies")
    suspend fun getPharmacies(): PharmacyResponse
}
```

### iOS (Swift)

```swift
struct APIConfig {
    static let baseURL = "https://KULLANICI_ADIN.pythonanywhere.com"
}

// Kullanım
let url = URL(string: "\(APIConfig.baseURL)/api/pharmacies")!
```

### React Native

```javascript
const API_BASE_URL = 'https://KULLANICI_ADIN.pythonanywhere.com';

export const fetchPharmacies = async () => {
  const response = await fetch(`${API_BASE_URL}/api/pharmacies`);
  return await response.json();
};
```

### Flutter

```dart
class ApiService {
  static const String baseUrl = 
    'https://KULLANICI_ADIN.pythonanywhere.com';
  
  Future<List<Pharmacy>> fetchPharmacies() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/pharmacies')
    );
    // ...
  }
}
```

---

## 🔄 Veriyi Güncelleme

HTML dosyası eskidiğinde (nöbet değiştiğinde):

### Yöntem 1: Manuel (Kolay)

1. PythonAnywhere → **Files**
2. `page_full.html` dosyasını sil
3. Yeni HTML'i yükle
4. **Web** → **Reload**

### Yöntem 2: API ile (Otomatik)

Lokal bilgisayardan:

```python
import requests

# Yeni veriyi çek
from nobet_scraper_selenium import fetch_nobet_list_selenium
new_html = open('selenium_page.html').read()

# PythonAnywhere'e gönder
requests.post(
    'https://KULLANICI_ADIN.pythonanywhere.com/api/update',
    json={'html': new_html}
)
```

---

## 🆘 Sorun Giderme

### "Application Error" Görüyorum

1. **"Web"** → **"Error log"** kontrol et
2. WSGI dosyasında kullanıcı adını doğru yazdın mı?
3. `api_server_simple.py` dosyası yüklü mü?

### Veri Gelmiyor

1. `page_full.html` dosyası yüklü mü?
2. **Files** sekmesinde dosyaları kontrol et
3. **Consoles** → **Bash**:
```bash
ls -la
```

### Kütüphane Hatası

```bash
pip3 install --user --upgrade flask flask-cors beautifulsoup4 requests
```

---

## 📊 Sonuç

✅ **API Adresi:**
```
https://KULLANICI_ADIN.pythonanywhere.com
```

✅ **Endpoint'ler:**
- `GET /api/pharmacies` - Tüm eczaneler
- `GET /api/pharmacies/merkez` - Merkez eczaneleri
- `GET /api/pharmacies/ermenek` - Ermenek eczaneleri
- `POST /api/refresh` - Cache yenile
- `POST /api/update` - HTML güncelle

✅ **Mobil uygulamadan kullanmaya hazır!**

---

## 🎯 Özet

| Adım | Süre | Durum |
|------|------|-------|
| Hesap aç | 2 dk | ✅ |
| Dosya yükle | 1 dk | ✅ |
| Kütüphane kur | 1 dk | ✅ |
| Web app oluştur | 1 dk | ✅ |
| WSGI düzenle | 30 sn | ✅ |
| Başlat | 10 sn | ✅ |
| **TOPLAM** | **~5 dk** | 🎉 |

**Şimdi mobil uygulamandan kullanabilirsin!** 📱







