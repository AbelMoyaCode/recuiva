#!/bin/bash

echo "🔍 DIAGNÓSTICO COMPLETO - RECUIVA BACKEND"
echo "========================================"
echo ""

echo "1️⃣ Verificando contenedor backend..."
docker ps | grep backend

echo ""
echo "2️⃣ Últimos logs del backend..."
docker-compose logs backend --tail=20

echo ""
echo "3️⃣ Probando endpoint de generación..."
curl -X POST "https://api-recuiva.duckdns.org/api/materials/c2e9dc80-6abd-4475-9ddf-dc2770441685/generate-questions" \
  -H "Content-Type: application/json" \
  -d '{"num_questions": 1, "strategy": "diverse"}' \
  2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ Pregunta generada:', data['questions'][0]['question'] if data.get('questions') else 'ERROR'); print('📊 Entidades:', data['questions'][0].get('concepts', []) if data.get('questions') else 'N/A'); print('🔍 Reasoning:', json.dumps(data['questions'][0].get('reasoning', {}), indent=2, ensure_ascii=False) if data.get('questions') else 'N/A')"

echo ""
echo "✅ Diagnóstico completado"
