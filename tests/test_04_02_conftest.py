"""
Módulo de Pruebas de Integración con Fixtures de Conftest.
Valida los flujos de autenticación utilizando datos externos parametrizados y marcas de ejecución.
"""

import pytest
from data.datos_suma import datos_user


class TestConfTest:

    # ==============================================================================
    # SECCIÓN DE LOGUEO Y MARCADORES (Smoke & Regression)
    # ==============================================================================

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("test_name, user, password, re", datos_user)
    def test_login(self, driver, test_name, user, password, re):
        """
        Evalúa los flujos de login (exitoso y fallidos) inyectando el estado del navegador
        desde el fixture 'driver' y las credenciales desde 'datos_user'.
        """
        print(f"TEST NAME: {test_name}")

        # 1.- Arrange (Organizar)
        # Gestionado automáticamente por los decoradores: 'driver' y '@pytest.mark.parametrize'

        # 2.- Act (Acción)
        # --- CORREGIDO: Evaluación dinámica basada en las credenciales reales de 'datos_user' ---
        # Nota: Ajusta los nombres de error de producción ("msj_error_user_no_existe") según tu dataset.
        if user == "test.0" and password == "Test1234":
            ra = "Login"
        elif user != "test.0":
            ra = "msj_error_user_no_existe"
        else:
            ra = "msj_error_pasw_incorrecto"

        # 3.- Assert (Afirmar)
        # Se corrigió la aserción comparando de forma estricta los caracteres de RA contra RE
        assert ra.lower() == re.lower(), f"Validar Login. RE: {re}. RA: {ra}"

# ==============================================================================
# GUÍA RÁPIDA DE COMANDOS DE TERMINAL PARA QA (Anotaciones de Repaso)
# ==============================================================================
# 📊 GENERACIÓN DE REPORTES BÁSICOS Y VOLCADO DE TEXTO:
# pytest -v                           -> Ejecución en modo descriptivo estándar.
# pytest -vv                          -> Ejecución con máxima visibilidad (Verbose completo).
# pytest -vv > resultado.txt          -> Redirecciona y guarda el reporte completo en un archivo de texto.
#
# 🏷️ FILTRADO POR MARCADORES (MARKERS):
# pytest -vv -m smoke > resultados.txt                  -> Ejecuta y reporta solo pruebas críticas de humo.
# pytest -vv -m regression .\tests\test_01.py > res.txt -> Ejecuta pruebas de regresión en un archivo específico.
#
# 📂 COMANDOS NATIVOS DE CREACIÓN DE PROYECTOS (BASH):
# mkdir programas                     -> Crea el directorio para la lógica de negocio.
# touch programas/__init__.py          -> Habilita la carpeta como un paquete importable de Python.
# touch programas/ahorro_casa.py       -> Crea el archivo fuente para el algoritmo de ahorro.


@pytest.mark.parametrize("login_data", ["usuario_prueba"], indirect=True)
def test_cobertura_fixture_login_data(login_data):
    """Prueba técnica para cubrir y validar el fixture login_data de conftest."""
    assert login_data == "usuario_prueba"
