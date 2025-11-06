@echo off
echo ================================================
echo  INICIANDO RECUIVA - SISTEMA COMPLETO
echo ================================================
echo.

REM Verificar que estamos en el directorio correcto
cd /d "%~dp0"
echo [1/4] Directorio actual: %CD%
echo.

REM Iniciar Backend en una nueva ventana
echo [2/4] Iniciando Backend en puerto 8000...
start "Recuiva Backend" cmd /k "cd backend && python main.py"
timeout /t 3 /nobreak >nul
echo      Backend iniciado
echo.

REM Iniciar Frontend en una nueva ventana DESDE public/
echo [3/4] Iniciando Frontend en puerto 5500...
start "Recuiva Frontend" cmd /k "cd public && python -m http.server 5500"
timeout /t 2 /nobreak >nul
echo      Frontend iniciado
echo.

REM Abrir el navegador
echo [4/4] Abriendo navegador...
timeout /t 3 /nobreak >nul
start http://localhost:5500/app/dashboard.html
echo      Navegador abierto
echo.

echo ================================================
echo  RECUIVA INICIADO CORRECTAMENTE
echo ================================================
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5500
echo   Dashboard: http://localhost:5500/app/dashboard.html
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
echo (Los servidores seguiran corriendo en sus propias ventanas)
pause >nul
