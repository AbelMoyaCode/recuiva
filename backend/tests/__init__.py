"""
═══════════════════════════════════════════════════════════════════════════════
MÓDULO DE PRUEBAS UNITARIAS - RECUIVA BACKEND
═══════════════════════════════════════════════════════════════════════════════

Este módulo contiene todas las pruebas unitarias para validar el funcionamiento
correcto de los componentes core del sistema RECUIVA.

ESTRUCTURA DE PRUEBAS:
├── test_hybrid_validator.py   → Validación semántica híbrida (BM25 + Cosine + Coverage)
├── test_embeddings.py         → Generación y similitud de embeddings
├── test_chunking.py           → Fragmentación de texto y extracción de PDF
├── test_sm2_algorithm.py      → Algoritmo de repetición espaciada SM-2
├── test_groq_api.py           → Generación de preguntas con IA (Groq API)
└── test_integration.py        → Pruebas de integración del flujo completo

EJECUCIÓN:
    # Ejecutar todas las pruebas
    pytest backend/tests/ -v

    # Ejecutar prueba específica
    pytest backend/tests/test_embeddings.py -v

    # Con cobertura
    pytest backend/tests/ --cov=backend --cov-report=html

MÉTRICAS OBJETIVO (según Project Charter):
- Cobertura de embeddings: ≥ 95%
- Precisión de recuperación top-3: ≥ 85%
- Tiempo de validación: ≤ 500ms
- Precisión HybridValidator: ≥ 75%

Autor: Abel Jesús Moya Acosta
Proyecto: RECUIVA - Taller Integrador I (UPAO)
Fecha: 5 de diciembre de 2025
═══════════════════════════════════════════════════════════════════════════════
"""

__version__ = "1.0.0"
__author__ = "Abel Jesús Moya Acosta"
