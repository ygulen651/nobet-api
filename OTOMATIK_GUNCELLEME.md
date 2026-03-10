# 🔄 Otomatik Güncelleme Rehberi

## 📊 Güncelleme Seçenekleri

| Yöntem | Kolaylık | Otomatik | Maliyet |
|--------|----------|----------|---------|
| **Manuel** | ⭐⭐⭐⭐⭐ | ❌ | ✅ Ücretsiz |
| **Lokal Script + Zamanlayıcı** | ⭐⭐⭐⭐ | ✅ | ✅ Ücretsiz |
| **Render.com** | ⭐⭐⭐ | ✅ | ✅ Ücretsiz |
| **PythonAnywhere Pro** | ⭐⭐⭐⭐⭐ | ✅ | ❌ $5/ay |

---

## 🟢 Yöntem 1: Manuel Güncelleme (Basit)

### Ne Zaman?
Nöbet listesi değiştiğinde (genellikle haftalık)

### Adımlar:

1. **Bilgisayarında:**
```bash
python nobet_scraper_selenium.py
# Menüden "1" seç (Selenium)
```

2. **Yeni HTML oluştu:** `selenium_page.html`

3. **PythonAnywhere:**
   - Files sekmesi
   - `page_full.html` → Sil
   - `selenium_page.html` → Yükle → Adını `page_full.html` yap
   - Web → Reload

⏱️ **5 dakika**

---

## 🟡 Yöntem 2: Otomatik Script (Önerilen)

### Nasıl Çalışır?

1. Bilgisayarında script çalışır
2. Web sitesinden yeni veri çeker
3. PythonAnywhere'e otomatik gönderir
4. API güncellenir

### Kurulum:

#### 1. Script Hazır:

`update_pythonanywhere.py` dosyası hazır!

#### 2. Test Et:

```bash
python update_pythonanywhere.py
```

✅ "Güncelleme başarılı!" göreceksin.

#### 3. Haftalık Otomatik Çalıştır:

### Windows Görev Zamanlayıcı

1. **Windows'ta ara:** "Görev Zamanlayıcı" (Task Scheduler)

2. **"Temel Görev Oluştur"** tıkla

3. **Ayarlar:**
   - **Ad:** Nöbetçi Eczane Güncelleme
   - **Tetikleyici:** Haftalık
   - **Gün:** Pazartesi
   - **Saat:** 09:00
   - **İşlem:** Program başlat
   - **Program:** `python`
   - **Argüman:** `"C:\Users\ugiaj\Desktop\nöbet\update_pythonanywhere.py"`
   - **Başlangıç:** `C:\Users\ugiaj\Desktop\nöbet`

4. **Bitti!**

Her Pazartesi sabah 9'da otomatik çalışacak! 🎉

---

### macOS/Linux (Cron)

```bash
# Crontab'ı düzenle
crontab -e

# Her Pazartesi 09:00
0 9 * * 1 cd /path/to/nobet && python3 update_pythonanywhere.py
```

---

## 🔵 Yöntem 3: Render.com (Tamamen Otomatik)

Render.com kullanırsan Selenium çalışır, günlük otomatik güncelleme yapabilir.

### Avantajlar:
- ✅ Tamamen otomatik
- ✅ Bilgisayar kapalı olsa bile çalışır
- ✅ Ücretsiz

### Dezavantajlar:
- ⚠️ GitHub gerekir
- ⚠️ Biraz daha teknik

---

## 🟣 Yöntem 4: PythonAnywhere Pro

**Aylık $5** ödersen:
- ✅ Zamanlanmış görevler
- ✅ Selenium çalışır
- ✅ Otomatik güncellemeler

---

## 📅 Güncelleme Sıklığı

### Nöbet Değişim Takvimi:

Karaman Eczacı Odası genellikle:
- **Günlük değişir** (bazı eczaneler)
- **Haftalık kontrol et**

### Tavsiye:

**Her Pazartesi sabah** güncelle → Tüm hafta güncel kalır.

---

## 🆘 Sorun Giderme

### Script Çalışmıyor

```bash
# Kütüphaneleri kontrol et
pip install selenium requests

# Chrome yüklü mü?
# ChromeDriver güncel mi?
```

### PythonAnywhere Güncellenmiyor

API endpoint doğru mu?
```python
PYTHONANYWHERE_API = "https://yusuf7007.pythonanywhere.com/api/update"
```

### Görev Zamanlayıcı Çalışmıyor

- Python yolu doğru mu?
- Script dosya yolu doğru mu?
- Bilgisayar açık mı? (uyku modunda çalışmaz)

---

## 🎯 Tavsiyem

### Başlangıç:
**Manuel güncelleme** (5 dakika, haftalık)

### İlerleyen Dönem:
**Otomatik script + Görev Zamanlayıcı** (Bir kez kur, unut!)

### Production:
**Render.com** (Bilgisayar kapansa bile çalışır)

---

## 📱 Mobil Uygulamada

API her zaman aynı adreste:
```
https://yusuf7007.pythonanywhere.com/api/pharmacies
```

Mobil uygulama her açıldığında güncel veriyi çeker.

Veri kaynağı (HTML) ne zaman güncellenirse, API otomatik yeni veriyi döner (5 dakika cache var).

