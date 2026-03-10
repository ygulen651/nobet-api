@echo off
setlocal
chcp 65001 > nul

echo ======================================================
echo    NOBETCI ECZANE - TAM OTOMATIK BULUT YUKLEME
echo ======================================================
echo.
echo 1. Git ayarlanıyor...
git init
git add .
git commit -m "Bulut otomasyonu aktifleştirildi"
git branch -M main

echo.
echo 2. GitHub bağlantısı kuruluyor...
:: Eski bağlantı varsa temizle
git remote remove origin >nul 2>&1
git remote add origin https://github.com/ygulen651/nobet-api.git

echo.
echo 3. Kodlar GitHub'a gönderiliyor...
echo [NOT] Eğer kullanıcı adı/şifre sorarsa lütfen giriş yap.
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [HATA] Yükleme sırasında bir sorun oluştu. 
    echo Lütfen internet bağlantını ve GitHub reposunu kontrol et.
) else (
    echo.
    echo ======================================================
    echo 🎉 İŞLEM TAMAM! 
    echo Artık bilgisayarın kapalı olsa da sistem çalışacak.
    echo ======================================================
)

echo.
echo Bu pencereyi kapatabilirsin.
pause