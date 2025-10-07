# Script de conexión SSH al Droplet de DigitalOcean
# Recuiva - Sistema de Active Recall con IA

Write-Host "🌊 Conectando al servidor DigitalOcean..." -ForegroundColor Cyan
Write-Host ""

# Pide la IP del Droplet
$IP = Read-Host "Ingresa la IP pública de tu Droplet"

if ([string]::IsNullOrWhiteSpace($IP)) {
    Write-Host "❌ Error: Debes ingresar una IP válida" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "📝 Conectando a root@$IP..." -ForegroundColor Green
Write-Host "   (Usa la contraseña que configuraste en DigitalOcean)" -ForegroundColor Yellow
Write-Host ""

# Conecta por SSH
ssh root@$IP
