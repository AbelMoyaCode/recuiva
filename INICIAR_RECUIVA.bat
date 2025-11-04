@echo off
echo ================================================
echo   RECUIVA - Sistema de Active Recall
echo   Iniciando servidores locales...
echo ================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo [1/4] Iniciando Backend FastAPI (puerto 8000)...
start "RECUIVA BACKEND" cmd /k "cd /d C:\Users\Abel\Desktop\recuiva && venv\Scripts\activate && cd backend && python main.py"

REM Esperar 4 segundos para que el backend inicie
timeout /t 4 /nobreak >nul

echo [2/4] Iniciando Frontend (puerto 3000)...
start "RECUIVA FRONTEND" cmd /k "cd /d C:\Users\Abel\Desktop\recuiva\public && python -m http.server 3000"

REM Esperar 3 segundos
timeout /t 3 /nobreak >nul

echo [3/4] Abriendo navegador...
start http://localhost:3000/

echo [4/4] Listo!
echo.
echo ================================================
echo   SERVIDORES CORRIENDO
echo ================================================
echo.
echo  Backend FastAPI:  http://localhost:8000
echo  Documentacion:    http://localhost:8000/docs
echo  Frontend:         http://localhost:3000/
echo  Crear Cuenta:     http://localhost:3000/app/auth/crear-cuenta.html
echo  Iniciar Sesion:   http://localhost:3000/app/auth/iniciar-sesion.html
echo  Dashboard:        http://localhost:3000/app/dashboard.html
echo.
echo ================================================
echo  IMPORTANTE: NO CIERRES ESTA VENTANA
echo  Para detener los servidores, cierra las ventanas
echo  "RECUIVA BACKEND" y "RECUIVA FRONTEND"
echo ================================================
echo.
pause
