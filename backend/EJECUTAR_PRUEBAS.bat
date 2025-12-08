@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM EJECUTAR_PRUEBAS.bat - Script para ejecutar pruebas de RECUIVA
REM ═══════════════════════════════════════════════════════════════════════════════
REM 
REM Uso:
REM   EJECUTAR_PRUEBAS.bat              - Ejecuta todos los tests
REM   EJECUTAR_PRUEBAS.bat embeddings   - Solo tests de embeddings
REM   EJECUTAR_PRUEBAS.bat validator    - Solo tests del validador
REM   EJECUTAR_PRUEBAS.bat quick        - Tests rápidos (sin slow)
REM   EJECUTAR_PRUEBAS.bat coverage     - Con reporte de cobertura
REM
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ════════════════════════════════════════════════════════════════════
echo 🧪 RECUIVA - Suite de Pruebas Unitarias
echo ════════════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no encontrado en PATH
    echo    Por favor, instala Python o activa tu entorno virtual
    pause
    exit /b 1
)

REM Verificar que pytest está instalado
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ pytest no está instalado. Instalando...
    pip install pytest pytest-cov
)

REM Procesar argumentos
if "%1"=="" goto :all
if "%1"=="all" goto :all
if "%1"=="embeddings" goto :embeddings
if "%1"=="validator" goto :validator
if "%1"=="chunking" goto :chunking
if "%1"=="sm2" goto :sm2
if "%1"=="groq" goto :groq
if "%1"=="quick" goto :quick
if "%1"=="coverage" goto :coverage
if "%1"=="integration" goto :integration
goto :help

:all
echo 📋 Ejecutando TODOS los tests...
echo.
python -m pytest tests/ -v --tb=short
goto :end

:embeddings
echo 📋 Ejecutando tests de EMBEDDINGS...
echo.
python -m pytest tests/test_embeddings.py -v --tb=short
goto :end

:validator
echo 📋 Ejecutando tests del VALIDADOR HÍBRIDO...
echo.
python -m pytest tests/test_hybrid_validator.py -v --tb=short
goto :end

:chunking
echo 📋 Ejecutando tests de CHUNKING...
echo.
python -m pytest tests/test_chunking.py -v --tb=short
goto :end

:sm2
echo 📋 Ejecutando tests del ALGORITMO SM-2...
echo.
python -m pytest tests/test_sm2_algorithm.py -v --tb=short
goto :end

:groq
echo 📋 Ejecutando tests de GROQ API...
echo.
python -m pytest tests/test_groq_api.py -v --tb=short -m "not requires_api"
goto :end

:quick
echo 📋 Ejecutando tests RÁPIDOS (sin slow)...
echo.
python -m pytest tests/ -v --tb=short -m "not slow"
goto :end

:coverage
echo 📋 Ejecutando tests con COBERTURA...
echo.
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
echo.
echo 📊 Reporte de cobertura generado en: htmlcov/index.html
goto :end

:integration
echo 📋 Ejecutando tests de INTEGRACIÓN...
echo.
python -m pytest tests/test_integration.py -v --tb=short
goto :end

:help
echo.
echo Uso: EJECUTAR_PRUEBAS.bat [opción]
echo.
echo Opciones:
echo   (vacío)     - Ejecuta todos los tests
echo   all         - Ejecuta todos los tests
echo   embeddings  - Solo tests de embeddings
echo   validator   - Solo tests del validador híbrido
echo   chunking    - Solo tests de chunking
echo   sm2         - Solo tests del algoritmo SM-2
echo   groq        - Solo tests de Groq API
echo   quick       - Tests rápidos (excluye @slow)
echo   coverage    - Tests con reporte de cobertura
echo   integration - Tests de integración
echo.
goto :end

:end
echo.
echo ════════════════════════════════════════════════════════════════════
echo ✅ Ejecución completada
echo ════════════════════════════════════════════════════════════════════
echo.
pause
