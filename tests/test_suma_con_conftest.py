"""
Módulo de Pruebas Unitarias para Operaciones Matemáticas utilizando Conftest.
Evalúa escenarios positivos, negativos y pruebas parametrizadas de suma de datos.
"""

import pytest

# --- CORREGIDO: Importación exacta apuntando a la carpeta 'src' y su módulo con mayúsculas ---
from src.OperacionesMatematicas import OperacionesMatematicas


class TestSumaConConftest:

    def test_suma_positivo(self, setup_datos_suma, hola_soy_conftest):
        """Prueba nominal utilizando el primer set de datos de signo positivo desde conftest."""
        # Arrange (Organizar)
        op = OperacionesMatematicas()

        # Leemos el índice 0 de la lista que retorna el fixture en tu conftest.py
        a = setup_datos_suma[0]['a']
        b = setup_datos_suma[0]['b']
        re = setup_datos_suma[0]['re']

        # Act (Acción)
        ra = op.suma(a, b)

        # Assert (Afirmar)
        assert ra == re, f"Validar suma. RE: {re}. RA: {ra}"

    def test_suma_negativo(self, setup_datos_suma, hola_soy_conftest):
        """Prueba nominal utilizando el segundo set de datos de signo negativo desde conftest."""
        # Arrange (Organizar)
        op = OperacionesMatematicas()

        # Leemos el índice 1 de la lista que retorna el fixture en tu conftest.py
        a = setup_datos_suma[1]['a']
        b = setup_datos_suma[1]['b']
        re = setup_datos_suma[1]['re']

        # Act (Acción)
        ra = op.suma(a, b)

        # Assert (Afirmar)
        assert ra == re, f"Validar suma negativa. RE: {re}. RA: {ra}"

    # --- CORREGIDO: Parametrización limpia de datos numéricos estructurados sin interferencias ---
    @pytest.mark.parametrize(
        "test_name, a, b, re",
        [
            ("Suma decimales", 1.5, 2.5, 4.0),
            ("Suma cero", 5, 0, 5),
            ("Suma mixta", -3, 8, 5)
        ]
    )
    def test_suma(self, test_name, a, b, re):
        """Prueba parametrizada orientada a evaluar múltiples casos de bordes numéricos."""
        print(f"Ejecutando test parametrizado: {test_name}")

        # Arrange (Organizar)
        op = OperacionesMatematicas()

        # Act (Acción)
        ra = op.suma(a, b)

        # Assert (Afirmar)
        assert ra == re, f"Validar la suma en escenario [{test_name}]. RA: {ra} RE: {re}"
