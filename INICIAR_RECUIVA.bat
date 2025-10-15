@echo off
echo ================================================
echo   RECUIVA - Sistema de Active Recall
echo ================================================
echo.
echo Iniciando servidores...
echo.

REM Iniciar Backend en una nueva ventana
start "RECUIVA BACKEND" cmd /k "cd /d C:\Users\Abel\Desktop\recuiva && venv\Scripts\activate && cd backend && python main.py"

REM Esperar 3 segundos para que el backend inicie
timeout /t 3 /nobreak >nul

REM Iniciar Frontend en otra ventana
start "RECUIVA FRONTEND" cmd /k "cd /d C:\Users\Abel\Desktop\recuiva\public && python -m http.server 5500"

REM Esperar 2 segundos
timeout /t 2 /nobreak >nul

REM Abrir navegador automáticamente
start http://localhost:5500/index.html

echo.
echo ================================================
echo   Servidores iniciados correctamente
echo ================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5500
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul
