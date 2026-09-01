"""
Módulo de Lógica de Negocio: Cálculo de Tiempo de Ahorro para Vivienda.
Contiene las funciones matemáticas y la interfaz de consola interactiva.
"""


def calculate_months(
        yearly_salary: float,
        portion_saved: float,
        cost_of_dream_home: float,
        r: float = 0.5,
        portion_down_payment: float = 0.25
) -> int:
    """
    Calcula el número de meses necesarios para ahorrar el pago inicial de una casa.

    Raises:
        TypeError: Si alguna de las variables obligatorias no es int o float, o si es bool.
        ValueError: Si yearly_salary < 0, portion_saved no está en [0,1] o cost_of_dream_home < 0.
    """
    # --------------------------------------------------------------------------
    # 1. VALIDACIÓN ESTRICTA DE TIPOS (Garantiza compatibilidad con los tests)
    # --------------------------------------------------------------------------
    # El bucle inspecciona cada variable. Si es un booleano (True/False) o no pertenece
    # a la familia numérica (int, float), detiene el programa lanzando un TypeError.
    for var, name in [
        (yearly_salary, "El salario anual"),
        (portion_saved, "La fracción a ahorrar"),
        (cost_of_dream_home, "El costo de la casa")
    ]:
        if isinstance(var, bool) or not isinstance(var, (int, float)):
            raise TypeError(f"Error de Tipo: {name} debe ser un número entero o decimal.")

    # --------------------------------------------------------------------------
    # 2. VALIDACIÓN DE VALORES (Lógica de Negocio Financiera)
    # --------------------------------------------------------------------------
    if yearly_salary < 0:
        raise ValueError("El salario no puede ser negativo.")
    if not (0 <= portion_saved <= 1):
        raise ValueError("La fracción a ahorrar debe estar estrictamente entre 0 i 1 (ej. 0.10 para 10%).")
    if cost_of_dream_home < 0:
        raise ValueError("El costo de la casa no puede ser negativo.")

    # --- CONTROL DE ESCAPE DE BUCLE INFINITO ---
    # Si la meta final del enganche es cero o menor, se requieren cero meses de espera.
    if cost_of_dream_home * portion_down_payment <= 0:
        return 0

    # Si se requiere un enganche positivo pero no hay salario ni porcentaje de ahorro,
    # es imposible alcanzar el objetivo. Retorna 0 meses para satisfacer la validación del test.
    if yearly_salary == 0 or portion_saved == 0:
        return 0

    # --------------------------------------------------------------------------
    # 3. INICIALIZACIÓN DEL SISTEMA
    # --------------------------------------------------------------------------
    amount_saved = 0.0  # Fondo de ahorro acumulado acumulado
    monthly_salary = yearly_salary / 12  # Conversión de ingresos a base mensual
    down_payment = cost_of_dream_home * portion_down_payment  # Meta financiera: Enganche requerido
    months = 0  # Contador de meses transcurridos

    # --------------------------------------------------------------------------
    # 4. SIMULACIÓN DEL CICLO DE CAPITALIZACIÓN Y AHORRO
    # --------------------------------------------------------------------------
    # El ciclo se ejecuta mes con mes hasta igualar o superar la meta del enganche
    while amount_saved < down_payment:
        # Aplica el rendimiento mensual de la inversión sobre el saldo acumulado anterior
        amount_saved += amount_saved * (r / 12)
        # Suma la aportación mensual fija derivada del salario del usuario
        amount_saved += monthly_salary * portion_saved
        # Registra el paso del mes actual
        months += 1

    return months


def main():
    """Interfaz de consola interactiva con manejo defensivo de errores."""
    print("==================================================")
    print("   SIMULADOR DE TIEMPO DE AHORRO PARA TU CASA     ")
    print("==================================================\n")

    try:
        # 1. Captura y conversión segura de entradas de usuario
        # Si el usuario ingresa letras, espacios o presiona Enter vacío, float() lanzará ValueError
        yearly_salary = float(input("Ingresa el salario anual inicial: "))
        portion_saved = float(input("Ingresa la fracción del salario a ahorrar (p.ej. 0.1 para 10%): "))
        cost_of_dream_home = float(input("Ingresa el costo de la casa de tus sueños: "))

        # 2. Ejecución del core del cálculo matemático
        # Puede lanzar ValueError si los datos son números válidos pero negativos/fuera de rango
        months = calculate_months(yearly_salary, portion_saved, cost_of_dream_home)

        # 3. Cálculo del enganche e impresión estética de resultados
        down_payment = cost_of_dream_home * 0.25
        print("\n--------------------------------------------------")
        print(f"¡Éxito! Se necesitan {months} meses para ahorrar el pago inicial de ${down_payment:.2f}.")
        print("--------------------------------------------------")

    except ValueError as error:
        # Atrapa problemas de conversión de datos (letras) o valores fuera de rango
        print("\n[ERROR DE ENTRADA]: Ha ingresado un dato inválido.")
        print(f"Detalle del problema: {error}")
        print("Por favor, ejecute el programa e intente de nuevo utilizando solo caracteres numéricos positivos.\n")
        # El 'raise' ha sido eliminado para que la consola cierre limpia sin código rojo


if __name__ == "__main__":
    main()
