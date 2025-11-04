@echo off
chcp 65001 >nul
echo ============================================================
echo  Iniciando Backend Recuiva - FastAPI
echo ============================================================
echo.

cd /d "c:\Users\Abel\Desktop\recuiva\backend"

echo [INFO] Directorio actual: %CD%
echo [INFO] Verificando Python...
python --version
echo.

echo [INFO] Iniciando servidor en http://localhost:8000
echo [INFO] Documentación API: http://localhost:8000/docs
echo [INFO] Presiona Ctrl+C para detener
echo.

REM Iniciar con uvicorn directamente SIN reload
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info --no-access-log

echo.
echo Servidor detenido.
pause
