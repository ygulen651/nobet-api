#!/bin/bash
cd "$(dirname "$0")"
echo "======================================================"
echo "   NOBETCI ECZANE - TAM OTOMATIK BULUT YUKLEME (MAC)"
echo "======================================================"
python3 update_all.py
git add .
git commit -m "Veriler guncellendi (Mac Otomatik)"
git push origin main
echo "Islem tamamlandi. Kapatabilirsiniz."
read -p "Cikmak icin bir tusa basin..." -n1 -s
