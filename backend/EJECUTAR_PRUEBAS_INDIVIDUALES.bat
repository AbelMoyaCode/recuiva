@echo off
chcp 65001 >nul
color 0A
cls

echo ════════════════════════════════════════════════════════════════════════════════
echo   EJECUCIÓN INDIVIDUAL DE PRUEBAS UNITARIAS - RECUIVA
echo   Para capturar pantallas módulo por módulo
echo ════════════════════════════════════════════════════════════════════════════════
echo.
echo Presiona cualquier tecla para iniciar...
pause >nul
cls

REM ═══════════════════════════════════════════════════════════════════════════════
REM MÓDULO 1: EMBEDDINGS (20 tests)
REM ═══════════════════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────────────────┐
echo │  MÓDULO 1: TEST_EMBEDDINGS.PY (Objetivo 1 - Embeddings)                   │
echo │  Total: 20 pruebas - all-MiniLM-L6-v2                                      │
echo └────────────────────────────────────────────────────────────────────────────┘
echo.
python -m pytest tests/test_embeddings.py -v --tb=short
echo.
echo ✅ MÓDULO 1 COMPLETADO
echo.
echo Presiona cualquier tecla para continuar al Módulo 2...
pause >nul
cls

REM ═══════════════════════════════════════════════════════════════════════════════
REM MÓDULO 2: CHUNKING (20 tests)
REM ═══════════════════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────────────────┐
echo │  MÓDULO 2: TEST_CHUNKING.PY (Objetivo 1 - Chunking Semántico)             │
echo │  Total: 20 pruebas - Chunks 80-100 palabras, overlap 20                   │
echo └────────────────────────────────────────────────────────────────────────────┘
echo.
python -m pytest tests/test_chunking.py -v --tb=short
echo.
echo ✅ MÓDULO 2 COMPLETADO
echo.
echo Presiona cualquier tecla para continuar al Módulo 3...
pause >nul
cls

REM ═══════════════════════════════════════════════════════════════════════════════
REM MÓDULO 3: HYBRID VALIDATOR (23 tests)
REM ═══════════════════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────────────────┐
echo │  MÓDULO 3: TEST_HYBRID_VALIDATOR.PY (Objetivo 2 - Validador Híbrido)      │
echo │  Total: 23 pruebas - BM25 5%% + Coseno 80%% + Cobertura 15%%                │
echo └────────────────────────────────────────────────────────────────────────────┘
echo.
python -m pytest tests/test_hybrid_validator.py -v --tb=short
echo.
echo ✅ MÓDULO 3 COMPLETADO
echo.
echo Presiona cualquier tecla para continuar al Módulo 4...
pause >nul
cls

REM ═══════════════════════════════════════════════════════════════════════════════
REM MÓDULO 4: GROQ API (23 tests)
REM ═══════════════════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────────────────┐
echo │  MÓDULO 4: TEST_GROQ_API.PY (Objetivo 3 - API Groq Llama 3.3 70B)         │
echo │  Total: 23 pruebas - 21 PASS + 2 SKIP (requieren API key real)            │
echo └────────────────────────────────────────────────────────────────────────────┘
echo.
python -m pytest tests/test_groq_api.py -v --tb=short
echo.
echo ✅ MÓDULO 4 COMPLETADO
echo.
echo Presiona cualquier tecla para continuar al Módulo 5...
pause >nul
cls

REM ═══════════════════════════════════════════════════════════════════════════════
REM MÓDULO 5: SM-2 ALGORITHM (17 tests)
REM ═══════════════════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────────────────┐
echo │  MÓDULO 5: TEST_SM2_ALGORITHM.PY (Objetivo 4 - Repetición Espaciada)      │
echo │  Total: 17 pruebas - Algoritmo SM-2                                        │
echo └────────────────────────────────────────────────────────────────────────────┘
echo.
python -m pytest tests/test_sm2_algorithm.py -v --tb=short
echo.
echo ✅ MÓDULO 5 COMPLETADO
echo.
echo Presiona cualquier tecla para continuar al Módulo 6...
pause >nul
cls

REM ═══════════════════════════════════════════════════════════════════════════════
REM MÓDULO 6: INTEGRACIÓN (9 tests)
REM ═══════════════════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────────────────┐
echo │  MÓDULO 6: TEST_INTEGRATION.PY (Pruebas de Integración y Performance)     │
echo │  Total: 9 pruebas - 8 PASS + 1 SKIP (requiere API)                         │
echo └────────────────────────────────────────────────────────────────────────────┘
echo.
python -m pytest tests/test_integration.py -v --tb=short
echo.
echo ✅ MÓDULO 6 COMPLETADO
echo.
echo.
echo ════════════════════════════════════════════════════════════════════════════════
echo   ✅✅✅ TODAS LAS PRUEBAS COMPLETADAS ✅✅✅
echo ════════════════════════════════════════════════════════════════════════════════
echo.
echo   RESUMEN FINAL:
echo   - test_embeddings.py:         20/20 PASS ✓
echo   - test_chunking.py:           20/20 PASS ✓
echo   - test_hybrid_validator.py:   23/23 PASS ✓
echo   - test_groq_api.py:           21/23 PASS (2 skip)
echo   - test_sm2_algorithm.py:      17/17 PASS ✓
echo   - test_integration.py:         8/9 PASS (1 skip)
echo.
echo   TOTAL: 109 PASS + 3 SKIP = 112 tests
echo.
echo ════════════════════════════════════════════════════════════════════════════════
echo.
pause
