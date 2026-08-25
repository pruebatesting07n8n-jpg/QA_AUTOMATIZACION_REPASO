import re

import pytest

from src.OperacionesMatematicas import OperacionesMatematicas


class TestParametrized02:
    @pytest.mark.parametrize(
        "test_name, user, password, re",
        [
            ("Login Exitoso", "test.0", "Test1234", "login"),
            ("Login usuario no existente", "test.not.exit", "Test1234", "msj_error_user_no existe"),
            ("Login password incorrecto", "test.0", "passincorrecto", "msj_error_passw_incorrecto")
        ]
    )

    def test_login(self,test_name,user,password,re):
        print(f"Testing {test_name}")
        #Arrange
        #1.- Datos de prueba y re parametrizado

        #Act
        # 1.- Codigo Automatizado para hacer Login
        #2. recuperar RA
        # - puede ser mensaje
        # - puede ser objeto existente o no existente

        ra = "Login"

        #Assert
        assert ra == re, f"Validar Login. RE: {re}. RA:{ra}"

    @pytest.mark.parametrize(
        "test_name, a, b, tipo_error,mensaje_error",
        [
            ("Division sobre 0", 10, 0,ZeroDivisionError,"division by zero"),
            ("Division sobre None", 3, None, TypeError,"unsupported operand type(s) for //: 'int' and 'NoneType'")

        ]
    )
    def test_division(self,test_name,a,b,tipo_error,mensaje_error):
        print(f"Test {test_name}")
        op = OperacionesMatematicas()
        #raises no servira para ver lo de excepciones
        #regex es una expresion regular
        with pytest.raises(tipo_error,match=re.escape(mensaje_error)):
            op.division(a,b)

