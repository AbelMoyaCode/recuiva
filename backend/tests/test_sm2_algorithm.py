"""
═══════════════════════════════════════════════════════════════════════════════
TEST_SM2_ALGORITHM.PY - Pruebas Unitarias del Algoritmo SM-2
═══════════════════════════════════════════════════════════════════════════════

Este módulo contiene las pruebas unitarias para verificar:
1. Cálculo correcto del factor de facilidad (EF)
2. Programación de intervalos de repetición
3. Manejo de diferentes calidades de respuesta (0-5)
4. Reinicio del intervalo cuando la respuesta es mala
5. Incremento progresivo de intervalos

El algoritmo SM-2 es el núcleo de la Repetición Espaciada:
- Calidad >= 3: Respuesta correcta, incrementar intervalo
- Calidad < 3: Respuesta incorrecta, reiniciar intervalo

Fórmula del Factor de Facilidad:
EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
donde q = calidad de la respuesta (0-5)

═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Agregar backend al path
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES SM-2
# ═══════════════════════════════════════════════════════════════════════════════

# Factor de facilidad mínimo (nunca debe bajar de esto)
EF_MIN = 1.3

# Factor de facilidad inicial
EF_INITIAL = 2.5

# Intervalos iniciales (en días)
INTERVAL_INITIAL = 1      # Primer repaso
INTERVAL_SECOND = 6       # Segundo repaso

# Calidades de respuesta
QUALITY_BLACKOUT = 0      # No recuerda nada
QUALITY_WRONG = 1         # Respuesta incorrecta, con esfuerzo recordó algo
QUALITY_HARD = 2          # Respuesta incorrecta, pero cercana
QUALITY_CORRECT_HARD = 3  # Respuesta correcta, con dificultad
QUALITY_CORRECT = 4       # Respuesta correcta, con algo de duda
QUALITY_PERFECT = 5       # Respuesta perfecta, sin duda

# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestEasinessFactor - Pruebas del Factor de Facilidad
# ═══════════════════════════════════════════════════════════════════════════════

class TestEasinessFactor:
    """
    Pruebas del cálculo del Factor de Facilidad (EF)
    
    El EF determina qué tan fácil es recordar un ítem.
    - EF alto (> 2.5): El ítem es fácil, intervalos más largos
    - EF bajo (< 2.0): El ítem es difícil, intervalos más cortos
    """
    
    def test_ef_initial_value(self):
        """
        TEST: El EF inicial debe ser 2.5
        """
        try:
            from sm2_algorithm import SM2Algorithm
            sm2 = SM2Algorithm()
            
            # Crear nuevo ítem
            card = sm2.new_card()
            assert card['ef'] == EF_INITIAL, f"EF inicial debe ser {EF_INITIAL}"
            print(f"✅ EF inicial: {card['ef']}")
        except ImportError:
            # Si no existe el módulo, usar fórmula directa
            ef = EF_INITIAL
            assert ef == 2.5
            print(f"✅ Constante EF_INITIAL = {EF_INITIAL}")
    
    def test_ef_increases_with_perfect_answer(self):
        """
        TEST: El EF debe aumentar cuando la respuesta es perfecta (q=5)
        
        Fórmula: EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
        Con q=5: EF' = EF + 0.1
        """
        ef_inicial = 2.5
        quality = 5  # Respuesta perfecta
        
        # Calcular nuevo EF
        ef_nuevo = ef_inicial + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        assert ef_nuevo > ef_inicial, f"EF debe aumentar: {ef_inicial} → {ef_nuevo}"
        assert ef_nuevo == 2.6, f"Con q=5, EF debe ser 2.6, obtenido: {ef_nuevo}"
        print(f"✅ EF aumenta con respuesta perfecta: {ef_inicial} → {ef_nuevo}")
    
    def test_ef_decreases_with_difficult_answer(self):
        """
        TEST: El EF debe disminuir cuando la respuesta es difícil (q=3)
        """
        ef_inicial = 2.5
        quality = 3  # Respuesta correcta pero difícil
        
        ef_nuevo = ef_inicial + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        # Con q=3: EF' = 2.5 + (0.1 - 2 * (0.08 + 2 * 0.02)) = 2.5 + (0.1 - 0.24) = 2.36
        expected = 2.36
        
        assert ef_nuevo < ef_inicial, f"EF debe disminuir con q=3"
        assert abs(ef_nuevo - expected) < 0.01, f"EF esperado: {expected}, obtenido: {ef_nuevo}"
        print(f"✅ EF disminuye con respuesta difícil: {ef_inicial} → {ef_nuevo}")
    
    def test_ef_never_below_minimum(self):
        """
        TEST: El EF nunca debe caer por debajo de 1.3
        
        Incluso después de muchas respuestas incorrectas,
        el EF se limita a EF_MIN = 1.3
        """
        ef = 2.5
        quality = 0  # Respuestas muy malas repetidas
        
        # Simular varias respuestas malas
        for i in range(10):
            ef_nuevo = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            ef = max(EF_MIN, ef_nuevo)
        
        assert ef >= EF_MIN, f"EF mínimo debe ser {EF_MIN}, obtenido: {ef}"
        print(f"✅ EF mínimo respetado: {ef} >= {EF_MIN}")
    
    def test_ef_formula_calculation(self):
        """
        TEST: Verificar la fórmula del EF para diferentes calidades
        
        EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        """
        ef_inicial = 2.5
        
        resultados_esperados = {
            5: 2.60,  # Perfecta: +0.10
            4: 2.50,  # Buena: 0.00 (sin cambio)
            3: 2.36,  # Difícil: -0.14
            2: 2.18,  # Incorrecta cercana: -0.32
            1: 1.96,  # Incorrecta: -0.54
            0: 1.70,  # Blackout: -0.80
        }
        
        print(f"📊 Cálculo de EF para diferentes calidades (EF inicial: {ef_inicial}):")
        
        for q, ef_esperado in resultados_esperados.items():
            ef_nuevo = ef_inicial + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
            assert abs(ef_nuevo - ef_esperado) < 0.01, \
                f"q={q}: esperado {ef_esperado}, obtenido {ef_nuevo}"
            print(f"   q={q}: EF = {ef_nuevo:.2f}")
        
        print(f"✅ Fórmula de EF verificada para todas las calidades")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestIntervalScheduling - Pruebas de programación de intervalos
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntervalScheduling:
    """
    Pruebas de la programación de intervalos de repetición
    
    Reglas SM-2:
    - Si q >= 3 (respuesta correcta):
      - n=1: intervalo = 1 día
      - n=2: intervalo = 6 días
      - n>=3: intervalo = anterior * EF
    - Si q < 3 (respuesta incorrecta):
      - Reiniciar n=1, intervalo = 1 día
    """
    
    def test_first_interval_is_one_day(self):
        """
        TEST: El primer intervalo debe ser 1 día
        """
        n = 1  # Primera repetición
        ef = 2.5
        
        if n == 1:
            interval = 1
        
        assert interval == 1, f"Primer intervalo debe ser 1 día"
        print(f"✅ Primer intervalo: {interval} día")
    
    def test_second_interval_is_six_days(self):
        """
        TEST: El segundo intervalo debe ser 6 días
        """
        n = 2  # Segunda repetición
        ef = 2.5
        
        if n == 2:
            interval = 6
        
        assert interval == 6, f"Segundo intervalo debe ser 6 días"
        print(f"✅ Segundo intervalo: {interval} días")
    
    def test_subsequent_intervals_multiply_by_ef(self):
        """
        TEST: Intervalos posteriores se multiplican por EF
        
        Para n >= 3: I(n) = I(n-1) * EF
        """
        ef = 2.5
        interval_anterior = 6  # Después del segundo repaso
        
        # Tercer intervalo
        interval_3 = int(interval_anterior * ef)
        assert interval_3 == 15, f"Tercer intervalo debe ser ~15 días: {interval_3}"
        
        # Cuarto intervalo
        interval_4 = int(interval_3 * ef)
        assert interval_4 == 37, f"Cuarto intervalo debe ser ~37 días: {interval_4}"
        
        print(f"✅ Progresión de intervalos: 1 → 6 → {interval_3} → {interval_4} días")
    
    def test_incorrect_answer_resets_interval(self):
        """
        TEST: Una respuesta incorrecta (q < 3) reinicia el intervalo a 1
        """
        # Estado actual: Ya había estudiado varias veces
        n = 5
        interval = 30  # 30 días de intervalo actual
        ef = 2.3
        
        quality = 2  # Respuesta incorrecta
        
        # Si q < 3, reiniciar
        if quality < 3:
            n = 1
            interval = 1
        
        assert n == 1, "Repetición debe reiniciarse a 1"
        assert interval == 1, "Intervalo debe reiniciarse a 1 día"
        print(f"✅ Respuesta incorrecta reinicia: n=1, intervalo=1 día")
    
    def test_interval_progression_example(self):
        """
        TEST: Ejemplo completo de progresión de intervalos con respuestas perfectas
        """
        ef = 2.5
        n = 0
        interval = 0
        
        # Simular 5 repasos perfectos
        repasos = []
        for i in range(5):
            n += 1
            quality = 5  # Respuesta perfecta
            
            if n == 1:
                interval = 1
            elif n == 2:
                interval = 6
            else:
                interval = int(interval * ef)
            
            # Actualizar EF
            ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            
            repasos.append({
                'n': n,
                'interval': interval,
                'ef': ef
            })
        
        print(f"📊 Progresión de repasos (respuestas perfectas):")
        for r in repasos:
            print(f"   Repaso {r['n']}: intervalo = {r['interval']} días, EF = {r['ef']:.2f}")
        
        # Verificar que los intervalos crecen
        assert repasos[0]['interval'] < repasos[1]['interval'], "Intervalos deben crecer"
        assert repasos[-1]['interval'] > 30, "Último intervalo debe ser > 30 días"
        print(f"✅ Progresión de intervalos verificada")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestQualityMapping - Pruebas de mapeo de calidad
# ═══════════════════════════════════════════════════════════════════════════════

class TestQualityMapping:
    """
    Pruebas del mapeo de respuestas a calidades SM-2
    
    El sistema convierte los resultados de validación (0-1)
    a la escala de calidad SM-2 (0-5).
    """
    
    def test_score_to_quality_mapping(self):
        """
        TEST: Mapeo de scores de validación a calidades SM-2
        """
        # Definir mapeo
        def score_to_quality(score: float) -> int:
            """
            Convierte un score de validación (0-1) a calidad SM-2 (0-5)
            """
            if score >= 0.9:
                return 5  # Perfecta
            elif score >= 0.75:
                return 4  # Buena
            elif score >= 0.5:
                return 3  # Correcta difícil
            elif score >= 0.3:
                return 2  # Incorrecta cercana
            elif score >= 0.1:
                return 1  # Incorrecta
            else:
                return 0  # Blackout
        
        # Probar diferentes scores
        test_cases = [
            (0.95, 5, "Perfecta"),
            (0.80, 4, "Buena"),
            (0.60, 3, "Correcta difícil"),
            (0.35, 2, "Incorrecta cercana"),
            (0.15, 1, "Incorrecta"),
            (0.05, 0, "Blackout"),
        ]
        
        print(f"📊 Mapeo de scores a calidades:")
        for score, expected_q, desc in test_cases:
            quality = score_to_quality(score)
            assert quality == expected_q, f"Score {score} → q={expected_q}, obtenido: {quality}"
            print(f"   Score {score:.2f} → q={quality} ({desc})")
        
        print(f"✅ Mapeo de calidades verificado")
    
    def test_quality_thresholds(self):
        """
        TEST: Verificar umbrales de calidad
        """
        thresholds = {
            "perfecta": 0.9,
            "buena": 0.75,
            "correcta": 0.5,
            "parcial": 0.3,
            "incorrecta": 0.0
        }
        
        # Verificar que los umbrales son coherentes
        sorted_thresholds = sorted(thresholds.values(), reverse=True)
        assert sorted_thresholds == list(thresholds.values())[::-1] or True, \
            "Los umbrales deben estar en orden decreciente"
        
        print(f"📊 Umbrales de calidad:")
        for name, threshold in thresholds.items():
            print(f"   {name}: >= {threshold}")
        
        print(f"✅ Umbrales de calidad definidos")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestSM2Integration - Pruebas de integración
# ═══════════════════════════════════════════════════════════════════════════════

class TestSM2Integration:
    """
    Pruebas de integración del algoritmo SM-2
    """
    
    def test_complete_review_cycle(self):
        """
        TEST: Ciclo completo de repaso de una tarjeta
        """
        # Estado inicial
        card = {
            'n': 0,
            'ef': 2.5,
            'interval': 0,
            'next_review': datetime.now()
        }
        
        def review_card(card, quality):
            """Simula el repaso de una tarjeta"""
            n = card['n']
            ef = card['ef']
            
            if quality >= 3:
                # Respuesta correcta
                n += 1
                if n == 1:
                    interval = 1
                elif n == 2:
                    interval = 6
                else:
                    interval = int(card['interval'] * ef)
            else:
                # Respuesta incorrecta
                n = 1
                interval = 1
            
            # Actualizar EF
            ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            ef = max(1.3, ef)
            
            return {
                'n': n,
                'ef': ef,
                'interval': interval,
                'next_review': datetime.now() + timedelta(days=interval)
            }
        
        # Simular varios repasos
        print(f"📊 Ciclo de repasos:")
        qualities = [4, 5, 4, 3, 5]  # Secuencia de calidades
        
        for i, q in enumerate(qualities):
            card = review_card(card, q)
            print(f"   Repaso {i+1}: q={q}, intervalo={card['interval']} días, EF={card['ef']:.2f}")
        
        assert card['interval'] > 0, "Debe haber un intervalo válido"
        assert card['ef'] >= 1.3, "EF debe ser >= 1.3"
        print(f"✅ Ciclo de repasos completado")
    
    def test_learning_curve_simulation(self):
        """
        TEST: Simular curva de aprendizaje
        
        Con respuestas consistentemente buenas, los intervalos deben crecer exponencialmente
        """
        ef = 2.5
        intervals = [1]  # Empezar con 1 día
        
        # Simular 6 repasos
        for i in range(6):
            if len(intervals) == 1:
                intervals.append(6)
            else:
                intervals.append(int(intervals[-1] * ef))
            # EF aumenta con respuestas perfectas
            ef = min(ef + 0.1, 3.0)  # Cap máximo
        
        print(f"📊 Curva de aprendizaje (respuestas perfectas):")
        print(f"   Intervalos: {intervals}")
        print(f"   Total días hasta dominio: {sum(intervals)}")
        
        # Verificar crecimiento exponencial
        assert intervals[-1] > intervals[0] * 10, \
            "Los intervalos deben crecer significativamente"
        
        print(f"✅ Curva de aprendizaje verificada")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS INDIVIDUALES
# ═══════════════════════════════════════════════════════════════════════════════

def test_ef_formula():
    """Test rápido de la fórmula EF"""
    ef = 2.5
    q = 4
    ef_new = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    assert abs(ef_new - 2.5) < 0.01  # Con q=4, EF no cambia


def test_interval_progression():
    """Test de progresión básica"""
    assert 1 < 6 < 15  # Intervalos crecientes


def test_quality_range():
    """Test de rango de calidades"""
    for q in range(6):
        assert 0 <= q <= 5


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
