#!/bin/bash
# Script para verificar y exponer Dokploy en el puerto 3000

echo "🔍 Verificando servicios de Dokploy..."
docker service ls

echo ""
echo "🔍 Verificando contenedores en ejecución..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "🔍 Verificando si Traefik está exponiendo el puerto 3000..."
docker inspect $(docker ps -q --filter "name=traefik") 2>/dev/null | grep -A 5 "HostPort"

echo ""
echo "🔧 Verificando configuración de red de Dokploy..."
docker service inspect dokploy --format '{{json .Endpoint.Ports}}' | python3 -m json.tool 2>/dev/null || docker service inspect dokploy --format '{{json .Endpoint.Ports}}'

echo ""
echo "📝 Verificando logs de Dokploy (últimas 20 líneas)..."
docker service logs dokploy --tail 20

echo ""
echo "✅ Si ves el puerto 3000 publicado arriba, Dokploy está accesible en:"
echo "   http://147.182.226.170:3000"
echo ""
echo "❌ Si NO ves el puerto 3000, necesitamos reconfigurar Dokploy."
