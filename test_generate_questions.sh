#!/bin/bash

# Script para probar generación de preguntas
# Uso: bash test_generate_questions.sh

MATERIAL_ID="c2e9dc80-6abd-4475-9ddf-dc2770441685"
BACKEND_URL="https://api-recuiva.duckdns.org"

echo "🔍 Probando generación de preguntas..."
echo "Material ID: $MATERIAL_ID"
echo ""

curl -X POST "$BACKEND_URL/api/materials/$MATERIAL_ID/generate-questions" \
  -H "Content-Type: application/json" \
  -d '{
    "num_questions": 1,
    "strategy": "diverse"
  }' | python3 -m json.tool

echo ""
echo "✅ Prueba completada"
