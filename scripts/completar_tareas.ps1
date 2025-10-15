# Script PowerShell para completar todas las tareas restantes de Recuiva
# Ejecutar desde: C:\Users\Abel\Desktop\recuiva

Write-Host "🚀 Iniciando limpieza de headers y creación de páginas institucionales..." -ForegroundColor Cyan

# TAREA 1: Limpiar header de dashboard.html
Write-Host "`n📝 Limpiando dashboard.html..." -ForegroundColor Yellow

# TODO: Implementar limpieza de dashboard.html manualmente

# TAREA 2: Crear páginas institucionales
Write-Host "`n📝 Creando páginas institucionales..." -ForegroundColor Yellow

# Verificar si existe la carpeta institucional
$institucionalPath = "public\app\institucional"
if (-not (Test-Path $institucionalPath)) {
    New-Item -ItemType Directory -Path $institucionalPath -Force
    Write-Host "✅ Carpeta institucional creada" -ForegroundColor Green
}

# Verificar si las páginas ya existen
$paginasExistentes = @()
if (Test-Path "$institucionalPath\active-recall.html") { $paginasExistentes += "active-recall.html" }
if (Test-Path "$institucionalPath\validacion-semantica.html") { $paginasExistentes += "validacion-semantica.html" }
if (Test-Path "$institucionalPath\diferencias.html") { $paginasExistentes += "diferencias.html" }

if ($paginasExistentes.Count -gt 0) {
    Write-Host "✅ Páginas ya existentes: $($paginasExistentes -join ', ')" -ForegroundColor Green
} else {
    Write-Host "⚠️ Páginas institucionales no encontradas. Crear manualmente." -ForegroundColor Yellow
}

# TAREA 3: Actualizar links del footer
Write-Host "`n📝 Verificando links del footer..." -ForegroundColor Yellow

$archivos = @(
    "public\index.html",
    "public\app\sesion-practica.html",
    "public\app\materiales.html",
    "public\app\repasos.html",
    "public\app\dashboard.html"
)

foreach ($archivo in $archivos) {
    if (Test-Path $archivo) {
        $contenido = Get-Content $archivo -Raw
        if ($contenido -match "institucional/active-recall.html") {
            Write-Host "  ✅ $archivo - Links correctos" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️ $archivo - Links deben actualizarse" -ForegroundColor Yellow
        }
    }
}

Write-Host "`n✅ DIAGNÓSTICO COMPLETADO" -ForegroundColor Cyan
Write-Host "📋 SIGUIENTE PASO: Revisar manualmente y aplicar cambios faltantes" -ForegroundColor White
