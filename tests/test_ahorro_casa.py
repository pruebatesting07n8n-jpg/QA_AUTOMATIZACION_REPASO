"""
Módulo de Pruebas Unitarias para el Calculador de Ahorro de Vivienda.
Garantiza la robustez de tipos, rangos lógicos y precisión matemática de la función 'calculate_months'.
"""

import pytest
from programas.ahorro_casa import calculate_months


# ==============================================================================
# CONFIGURACIONES Y FIXTURES (Datos Compartidos)
# ==============================================================================

@pytest.fixture
def defaults():
    """
    Proporciona los valores por defecto del sistema financiero del programa.
    Evita la duplicación de datos duros (Hardcoding) en múltiples pruebas.
    """
    return {
        "r": 0.5,  # Tasa de rendimiento anual por defecto (50%)
        "portion_down_payment": 0.25  # Fracción requerida para el pago inicial (25%)
    }


# ==============================================================================
# SECCIÓN 1: PRUEBAS MATEMÁTICAS Y ESCENARIOS NOMINALES
# ==============================================================================

@pytest.mark.parametrize(
    "yearly_salary, portion_saved, cost_of_dream_home, expected_months",
    [
        (120, 1.0, 100, 3),  # Caso 1: Ahorro total con propiedad de bajo costo
        (120, 0.5, 120, 6),  # Caso 2: Ahorro parcial (50%) con salario bajo
        (1000, 0.25, 100, 2),  # Caso 3: Ahorro acelerado con salario medio
        (120000, 0.10, 150000, 24)  # Caso 4: Escenario estándar de mercado
    ]
)
def test_calculate_months_parametrized(
        yearly_salary, portion_saved, cost_of_dream_home, expected_months
):
    """Evalúa que los cálculos matemáticos de meses coincidan exactamente con las proyecciones."""

    # 1. Asegura que los datos de prueba sean numéricos válidos antes de la ejecución
    assert isinstance(yearly_salary, (float, int)), "yearly_salary debe ser numérico (float/int)"
    assert isinstance(portion_saved, (float, int)), "portion_saved debe ser numérico (float/int)"
    assert isinstance(cost_of_dream_home, (float, int)), "cost_of_dream_home debe ser numérico (float/int)"

    # 2. Ejecuta el algoritmo principal de cálculo
    months = calculate_months(yearly_salary, portion_saved, cost_of_dream_home)

    # 3. Valida la firma del contrato: la función siempre debe retornar un entero para los meses
    assert isinstance(months, int), "El valor retornado por la función debe ser estrictamente un entero (int)"

    # 4. Compara el resultado del ciclo contra la expectativa matemática estricta
    assert months == expected_months, f"Error matemático: se esperaban {expected_months} meses pero se obtuvieron {months}"


# ==============================================================================
# SECCIÓN 2: VALIDACIÓN DE TIPOS Y ESTRUCTURAS DE DATOS CONTROLADAS
# ==============================================================================

@pytest.mark.parametrize(
    "bad_salary, bad_saved, bad_home",
    [
        # --- Pruebas con cadenas de texto (str) ---
        ("120000", 0.10, 150000),
        (120000, "0.10", 150000),
        (120000, 0.10, "150000"),
        # --- Pruebas con estructuras de listas (list) ---
        ([120000], 0.10, 150000),
        (120000, [0.10], 150000),
        (120000, 0.10, [150000]),
        # --- Pruebas con estructuras de diccionarios (dict) ---
        ({"val": 120000}, 0.10, 150000),
        (120000, {"val": 0.10}, 150000),
        (120000, 0.10, {"val": 150000})
    ]
)
def test_calculate_months_wrong_types(bad_salary, bad_saved, bad_home):
    """Verifica que el uso de tipos no numéricos detenga el programa mediante un TypeError."""

    # El test pasa si el intérprete bloquea la operación matemática lanzando TypeError
    with pytest.raises(TypeError):
        calculate_months(bad_salary, bad_saved, bad_home)


# ==============================================================================
# 2. NUEVO TEST ESPECÍFICO PARA BOOLEANOS - ACTUALIZADO Y CORREGIDO
# ==============================================================================
@pytest.mark.parametrize(
    "bool_salary, bool_saved, bool_home",
    [
        (True, 0.10, 150000),   # Salario Booleano
        (120000, True, 150000), # Fracción Booleana
        (120000, 0.10, True)    # Costo Booleano
    ]
)
def test_calculate_months_accepts_booleans(bool_salary, bool_saved, bool_home):
    """
    Verifica que la función rechace explícitamente valores booleanos (True/False)
    lanzando un TypeError, protegiendo así la integridad de los datos numéricos.
    """
    # El test pasará a verde exitosamente porque tu función en ahorro_casa.py
    # bloquea con éxito los booleanos usando un TypeError.
    with pytest.raises(TypeError):
        calculate_months(bool_salary, bool_saved, bool_home)


# ==============================================================================
# SECCIÓN 3: CONTROL DE VALORES LÓGICOS E INTEGRIDAD FINANCIERA
# ==============================================================================

@pytest.mark.parametrize(
    "neg_salary, neg_saved, neg_home",
    [
        # --- Pruebas sobre la variable: yearly_salary ---
        (-50000, 0.10, 150000),
        (-1.0, 0.10, 150000),
        # --- Pruebas de desborde de rango sobre: portion_saved (Límite:) ---
        (120000, -0.01, 150000),  # Desborde inferior por negativo
        (120000, 1.01, 150000),  # Desborde superior (101%)
        (120000, 5.5, 150000),  # Desborde superior masivo (550%)
        # --- Pruebas sobre la variable: cost_of_dream_home ---
        (120000, 0.10, -100.0),
        (120000.0, 0.10, -500000.0)
    ]
)
def test_calculate_months_invalid_values(neg_salary, neg_saved, neg_home):
    """Asegura el disparo controlado de un ValueError ante datos de entrada fuera de la lógica financiera."""

    # Valida el correcto funcionamiento de las compuertas de seguridad 'if' de la función
    with pytest.raises(ValueError):
        calculate_months(neg_salary, neg_saved, neg_home)


@pytest.mark.parametrize(
    "yearly_salary, portion_saved, cost_of_dream_home, expected_months",
    [
        (0.0, 0.10, 100000.0, 0),  # Caso Límite: Sin ingresos (Requiere enganche de $0 o se mitiga a 0 meses)
        (120000.0, 0.0, 150000.0, 0),  # Caso Límite: Capacidad de ahorro de 0% (Verifica no caer en bucle infinito)
        (120000.0, 1.0, 150000.0, 3),  # Caso Límite: Capacidad de ahorro total (100%)
        (120000.0, 0.10, 0.0, 0)  # Caso Límite: Propiedad con costo de $0 (Meta cumplida de inmediato)
    ]
)
def test_calculate_months_allowed_limits(yearly_salary, portion_saved, cost_of_dream_home, expected_months):
    """Prueba los extremos exactos permitidos por las reglas del negocio de la aplicación."""

    months = calculate_months(yearly_salary, portion_saved, cost_of_dream_home)
    # Valida que el tiempo sea coherente con conditions de resolución inmediata (0 meses) o superiores
    assert months >= expected_months


@pytest.mark.parametrize(
    "empty_salary, empty_saved, empty_home",
    [
        ("", 0.10, 150000.0),  # Cadena vacía estándar
        ("   ", 0.10, 150000.0),  # Cadena compuesta por espacios vacíos
        (120000.0, "", 150000.0),
        (120000.0, "   ", 150000.0),
        (120000.0, 0.10, ""),
        (120000.0, 0.10, "   ")
    ]
)
def test_calculate_months_empty_inputs(empty_salary, empty_saved, empty_home):
    """Valida el manejo defensivo contra entradas vacías provenientes de interfaces de usuario."""

    # La inyección de texto sin formato numérico debe romper con un TypeError controlado
    with pytest.raises(TypeError):
        calculate_months(empty_salary, empty_saved, empty_home)


# ==============================================================================
# SECCIÓN 4: PARÁMETROS OPCIONALES Y CONTRATOS POR DEFECTO
# ==============================================================================

def test_calculate_months_with_default_arguments(defaults):
    """Comprueba que la firma de la función resuelva adecuadamente sus parámetros por defecto."""

    # 1. Ejecución enviando explícitamente los datos financieros del fixture defaults
    months_explicit = calculate_months(
        120000, 0.10, 150000,
        r=defaults["r"],
        portion_down_payment=defaults["portion_down_payment"]
    )

    # 2. Ejecución delegando la resolución en los valores predeterminados de la firma
    months_default = calculate_months(120000, 0.10, 150000)

    # 3. Ambos flujos de ejecución deben generar exactamente el mismo resultado


# ==============================================================================
# SECCIÓN 5: PRUEBAS DE INTERFAZ DE CONSOLA (Función main con capsys)
# ==============================================================================

def test_main_successful_flow(monkeypatch, capsys):
    """
    Simula un flujo de usuario completamente exitoso en la consola.
    Verifica que el programa lea las entradas correctamente y muestre el resultado esperado.
    """
    # 1. Respuestas simuladas que el usuario "escribirá" en la consola en orden estricto
    user_inputs = ["120000", "0.10", "150000"]

    # 2. Intercepta la función input() para inyectar nuestra lista
    inputs_iterator = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_iterator))

    # 3. Invoca la función main
    from programas.ahorro_casa import main
    main()

    # 4. Captura la salida impresa en la consola
    captured = capsys.readouterr()

    # 5. Comprueba los datos esperados en el texto final
    assert "Se necesitan 24 meses" in captured.out
    assert "$37500.00" in captured.out


@pytest.mark.parametrize(
    "invalid_inputs",
    [
        ["letras_en_salario", "0.10", "150000"],  # Error en el salario (Texto)
        ["120000", "no_un_numero", "150000"],  # Error en la fracción a ahorrar (Texto)
        ["120000", "0.10", ""],  # Error en el costo de la casa (Campo vacío)
        ["   ", "0.10", "150000"],  # Error en el salario (Espacios en blanco)
    ]
)
def test_main_invalid_user_inputs(monkeypatch, capsys, invalid_inputs):
    """
    Verifica que la función main maneje los errores de entrada de forma amigable.
    Usa capsys para comprobar el texto impreso sin requerir la detención por raise.
    """
    # 1. Inyectamos las entradas inválidas del escenario actual
    inputs_iterator = iter(invalid_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_iterator))

    # 2. Ejecutamos la función main del archivo de producción
    from programas.ahorro_casa import main
    main()

    # 3. Capturamos la pantalla de la terminal
    captured = capsys.readouterr()

    # 4. Validamos que el mensaje amigable de control de errores se muestre correctamente
    assert "[ERROR DE ENTRADA]: Ha ingresado un dato inválido." in captured.out
    assert "Por favor, ejecute el programa e intente de nuevo" in captured.out
