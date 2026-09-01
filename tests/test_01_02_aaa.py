import pytest
from src.OperacionesMatematicas import OperacionesMatematicas


class TestAAA02:
    @pytest.mark.parametrize(
         "test_name, a, b, re", [
    ("numeros_positivos", 3,4,7),
    ("numeros_negativos", -1, -1, -2),
    ("numeros_negativos", -1, +1, 0)

]
     )
    def test_suma(self, test_name, a, b, re):
         print(f"test:{test_name}")
         #Arrage
         op = OperacionesMatematicas()

         #Act
         ra = op.suma(a, b)

         #Asser
         assert ra == re, f"validar la suma.  RA:{ra} RE:{re}"



    @pytest.fixture
    def setup(self):
        return [
            {"test_name": "numeros positivos", "a":3, "b":4, "re":7},
            {"test_name": "numeros negativos", "a": -3, "b": -1, "re": -4}
        ]

    def test_suma_for(self, setup):
        for item in setup:
            # Arrange
            op = OperacionesMatematicas()

        a= setup[0]['a']
        b = setup[0]['b']
        re = setup[0]['re']
        #Act (Action)
        ra = op.suma(a, b)
        #Assert
        assert ra == re, f"validar suma. RE:{re}. RA:{ra}"

    def test_suma_numeros_positivos(self, setup):
        #Arrange
        op=OperacionesMatematicas()
        a = setup[0]['a']
        b = setup[0]['b']
        re = setup[0]['re']
        #Act (Action)
        ra = op.suma(a, b)
        #Assert
        assert ra == re, f"validar suma. RE:{re}. RA:{ra}"
    def test_suma_numeros_negativos(self, setup):
        op = OperacionesMatematicas()
        a = setup[1]['a']
        b = setup[1]['b']
        re = setup[1]['re']
        # Act (Action)
        ra = op.suma(a, b)
        # Assert
        assert ra == re, f"validar rest. RE:{re}. RA:{ra}"