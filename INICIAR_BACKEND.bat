@echo off
echo ============================================================
echo  Iniciando Backend de Recuiva
echo ============================================================
echo.

cd /d "%~dp0backend"

echo Verificando Python...
python --version
echo.

echo Iniciando servidor FastAPI...
echo Backend URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False)"

pause
