#!/bin/bash
cd "$(dirname "$0")"
echo "======================================================"
echo "   NOBETCI ECZANE API SUNUCUSU (MAC)"
echo "======================================================"
echo "API baslatiliyor... (Durdurmak icin bu pencereyi kapatin)"
python3 api_server.py
