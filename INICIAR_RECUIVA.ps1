# ================================================
#   RECUIVA - Sistema de Active Recall
# ================================================

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "   RECUIVA - Sistema de Active Recall" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Cyan

Write-Host "🚀 Iniciando servidores...`n" -ForegroundColor Yellow

# Iniciar Backend en una nueva ventana
Write-Host "📡 Iniciando Backend (FastAPI)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\Abel\Desktop\recuiva; .\venv\Scripts\activate; cd backend; python main.py"

# Esperar 3 segundos
Start-Sleep -Seconds 3

# Iniciar Frontend en otra ventana
Write-Host "🌐 Iniciando Frontend (HTTP Server)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\Abel\Desktop\recuiva\public; python -m http.server 5500"

# Esperar 2 segundos
Start-Sleep -Seconds 2

# Abrir navegador automáticamente
Write-Host "🌍 Abriendo navegador..." -ForegroundColor Green
Start-Process "http://localhost:5500/index.html"

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "   ✅ Servidores iniciados correctamente" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Cyan

Write-Host "Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:5500" -ForegroundColor Yellow
Write-Host "`nPresiona cualquier tecla para cerrar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
