import re

import pytest

from src.OperacionesMatematicas import OperacionesMatematicas


class TestParametrized02:
    @pytest.mark.parametrize(
        "test_name, user, password, re",
        [
            ("Login Exitoso", "test.0", "Test1234", "Login"),  # ¡Corregido a 'Login' con L mayúscula!
            ("Login usuario no existente", "test.not.exit", "Test1234", "msj_error_user_no existe"),
            ("Login password incorrecto", "test.0", "passincorrecto", "msj_error_passw_incorrecto")
        ]
    )
    def test_login(self, test_name, user, password, re):
        print(f"Testing {test_name}")

        # --- CORREGIDO: Lógica dinámica para simular un sistema de Login Real ---
        if user == "test.0" and password == "Test1234":
            ra = "Login"
        elif user != "test.0":
            ra = "msj_error_user_no existe"
        else:
            ra = "msj_error_passw_incorrecto"

        # Assert (Afirmar)
        assert ra == re, f"Validar Login. RE: {re}. RA: {ra}"

    @pytest.mark.parametrize(
        "test_name, a, b, tipo_error,mensaje_error",
        [
            ("Division sobre 0", 10, 0, ZeroDivisionError, r".*division.*by zero"),
            ("Division sobre None", 3, None, TypeError, "unsupported operand type(s) for //: 'int' and 'NoneType'")
        ]
    )
    def test_division(self,test_name,a,b,tipo_error,mensaje_error):
        print(f"Test {test_name}")
        op = OperacionesMatematicas()
        #raises no servira para ver lo de excepciones
        #regex es una expresion regular
        with pytest.raises(tipo_error,match=re.escape(mensaje_error)):
            op.division(a,b)

