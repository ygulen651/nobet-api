@echo off
setlocal
chcp 65001 > nul

echo ======================================================
echo    NOBETCI ECZANE - BULUTA YUKLEME (GITHUB)
echo ======================================================
echo.
echo Bu islem, bilgisayarin kapali olsa bile calisacak olan
echo "Bulut Otomasyonu"nu aktif etmek icin gereklidir.
echo.

:: Git kontrolu
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [HATA] Git yuklu degil! Lutfen once Git kur: https://git-scm.com/
    pause
    exit
)

:: Git islemleri
git init
git add .
git commit -m "Bulut otomasyonu eklendi"
git branch -M main

echo.
echo ------------------------------------------------------
echo SIMDI YAPMAN GEREKENLER:
echo 1. GitHub.com'da yeni bir repo olustur (ad Gecen: nobet-api)
echo 2. Asagidaki komutu kendine gore duzenleyip buraya yapistir:
echo    git remote add origin https://github.com/KULLANICI_ADIN/nobet-api.git
echo 3. Son olarak su komutu yaz: git push -u origin main
echo ------------------------------------------------------
echo.

pause
git remote add origin https://github.com/ygulen651/nobet-api.git