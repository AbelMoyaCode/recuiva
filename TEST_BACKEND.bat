@echo off
cd /d "c:\Users\Abel\Desktop\recuiva\backend"
echo Iniciando backend Recuiva en puerto 8000...
echo.
python -m uvicorn test_simple:app --host 0.0.0.0 --port 8000
pause
