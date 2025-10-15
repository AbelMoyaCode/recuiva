#!/bin/bash

# Script de instalación para servidor DigitalOcean
# Recuiva - Sistema de Active Recall con IA
# Autor: Abel Moya

echo "🚀 Iniciando configuración del servidor para Recuiva..."

# 1. Actualizar el sistema
echo "📦 Actualizando el sistema..."
apt update && apt upgrade -y

# 2. Instalar Docker
echo "🐳 Instalando Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# 3. Instalar Docker Compose
echo "🔧 Instalando Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 4. Verificar instalaciones
echo "✅ Verificando instalaciones..."
docker --version
docker-compose --version

# 5. Instalar Dokploy
echo "📱 Instalando Dokploy..."
curl -sSL https://dokploy.com/install.sh | sh

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "🌐 Accede a Dokploy en: http://$(curl -s ifconfig.me):3000"
echo ""
echo "📋 Próximos pasos:"
echo "  1. Abre tu navegador en la URL de arriba"
echo "  2. Crea tu cuenta admin en Dokploy"
echo "  3. Conecta tu repositorio de GitHub"
echo "  4. Configura el despliegue con docker-compose.yml"
echo ""
