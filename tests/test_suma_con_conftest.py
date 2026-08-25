from src.OperacionesMatematicas import OperacionesMatematicas
import data.datos_suma as datos
import pytest
class TestSumaConConftest:

    def test_suma_positivo(self,setup_datos_suma, hola_soy_conftest):
        #Arrange
        op = OperacionesMatematicas()
        a = setup_datos_suma[0]['a']
        b = setup_datos_suma[0]['b']
        re = setup_datos_suma[0]['re']

        #Act (Action)

        ra = op.suma(a,b)
        #Assert
        assert ra == re, f"Validar suma. RE {re}. RA {re}"

    def test_suma_negativo(self,setup_datos_suma,hola_soy_conftest):
        # Arrange
        op = OperacionesMatematicas()
        a = setup_datos_suma[1]['a']
        b = setup_datos_suma[1]['b']
        re = setup_datos_suma[1]['re']

        # Act (Action)

        ra = op.suma(a, b)
        # Assert
        assert ra == re
        f"Validar suma. RE {re}. RA {re}"

    @pytest.mark.parametrize(
        "test_name, a, b, re", datos.datos_suma,datos.datos_user
    )
    def test_suma(self, test_name, a, b, re):
        print(f"test:{test_name}")
        # Arrage
        op = OperacionesMatematicas()

        # Act
        ra = op.suma(a, b)

        # Asser
        assert ra == re, f"validar la suma.  RA:{ra} RE:{re}"

