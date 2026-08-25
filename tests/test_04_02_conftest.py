import pytest

from data.datos_suma import datos_user


class TestConfTest:

    #Test que prueba el nombre de usuario

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("test_name, user,password,re", datos_user)
    def test_login(self, driver, test_name, user,password,re):
        print(f"TEST NAME: {test_name}")
        #1.- Arrage -> fixture  y parametrize
        # -navegador, datos de prueba y re parametrizado

        #2.- Act
        # 2.1. Codigo de Automatizacion para hacer login
        # 2.2. recuperar RA
        # - puede ser un mensaje
        # - puede ser un objeto existente o no existente

        ra = "login"

        #Assert

        assert  ra == re, f"Validar Login, RE:{re}. RA_{ra}"

##para el reporte ingresamos en terminal
#pytest -v o pytest -vv
# para importar pytest -vv > resultado.txt
#para los marcaaodres se ingresa en terminal
#pytest -vv -m smoke > resultados.txt
#ejemplo pytest -vv -m regression .\tests\ejemplos.01> resultados.txt



