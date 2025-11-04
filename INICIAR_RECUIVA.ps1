# ================================================
#   RECUIVA - Sistema de Active Recall
#   Script de inicio automático (PowerShell)
# ================================================

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "   RECUIVA - Sistema de Active Recall" -ForegroundColor Green
Write-Host "   Iniciando servidores locales..." -ForegroundColor White
Write-Host "================================================`n" -ForegroundColor Cyan

# Verificar si Python está instalado
Write-Host "[1/5] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor instala Python 3.8+ desde https://python.org" -ForegroundColor Red
    pause
    exit 1
}

# Iniciar Backend
Write-Host "`n[2/5] Iniciando Backend FastAPI (puerto 8000)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\Abel\Desktop\recuiva; .\venv\Scripts\activate; cd backend; python main.py"

# Esperar 4 segundos
Write-Host "⏳ Esperando a que el backend inicie..." -ForegroundColor Gray
Start-Sleep -Seconds 4

# Iniciar Frontend
Write-Host "`n[3/5] Iniciando Frontend (puerto 3000)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\Abel\Desktop\recuiva\public; python -m http.server 3000"

# Esperar 3 segundos
Write-Host "⏳ Esperando a que el frontend inicie..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# Abrir navegador
Write-Host "`n[4/5] Abriendo navegador..." -ForegroundColor Green
Start-Process "http://localhost:3000/"

Write-Host "`n[5/5] ✅ Listo!" -ForegroundColor Green

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "   SERVIDORES CORRIENDO" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Cyan

Write-Host "📡 Backend FastAPI:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "📄 Documentación:    http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "🌐 Frontend:         http://localhost:3000/" -ForegroundColor Yellow
Write-Host "👤 Crear Cuenta:     http://localhost:3000/app/auth/crear-cuenta.html" -ForegroundColor Cyan
Write-Host "🔐 Iniciar Sesión:   http://localhost:3000/app/auth/iniciar-sesion.html" -ForegroundColor Cyan
Write-Host "📊 Dashboard:        http://localhost:3000/app/dashboard.html" -ForegroundColor Cyan

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "⚠️  IMPORTANTE: NO CIERRES ESTA VENTANA" -ForegroundColor Red
Write-Host "Para detener los servidores, cierra las ventanas" -ForegroundColor White
Write-Host "'powershell' que se abrieron" -ForegroundColor White
Write-Host "================================================`n" -ForegroundColor Cyan

Write-Host "Presiona cualquier tecla para cerrar esta ventana..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
