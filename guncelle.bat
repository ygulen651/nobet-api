@echo off
setlocal
chcp 65001 > nul
echo ======================================================
echo    NOBETCI ECZANE - OTOMATIK GUNCELLEME SISTEMI
echo ======================================================
echo.
echo 1. Web sitesinden guncel veriler cekiliyor...
echo 2. PythonAnywhere sunucusuna gonderiliyor...
echo.

:: %~dp0 mevcut dosyanin bulundugu klasoru temsil eder.
:: Turhce karakter sorununu onlemek icin dinamik yol kullaniyoruz.
"C:\Users\ugiaj\AppData\Local\Programs\Python\Python313\python.exe" "%~dp0update_pythonanywhere.py"

echo.
echo ======================================================
echo    ISLEM TAMAMLANDI!
echo ======================================================
echo.
echo Pencere 10 saniye icinde otomatik kapanacaktir...
timeout /t 10
