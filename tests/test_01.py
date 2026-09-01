import pytest

from src.OperacionesMatematicas import OperacionesMatematicas

class TestOperacionesMatematicas:
    op=OperacionesMatematicas()

    ##Para inciiar y cerrar el google chrome
    @pytest.fixture
    def navegador(self):
        print("Iniciando navegador")
        driver = webdriver.Chrome()
        yield driver
        print("Finalizando navegador")
        driver.quit()

    @pytest.fixture
    def setup_and_teardown(self):
        # Before -setup
        print(">> [function] Antes del test") #precondicion
        yield "dato función"
        #After - teardown
        print("<< [function] Despues del test")#poscondicion


    #@pytest.fixture
    @pytest.fixture(scope="module")
    def datos_numeros(self):
        # print("Antes de cada Test")
        print("Antes de cada File (MODULE)")
        return [
            {"numero1": 2, "numero2": 3, "resultado_esperado": 5},
            {"numero1": -2, "numero2": -3, "resultado_esperado": -5},
            {"numero1": 4, "numero2": 2, "resultado_esperado": 2},
            {"numero1": -4, "numero2": 2, "resultado_esperado": -6},
            {"numero1": 4, "numero2": 2, "resultado_esperado": 8},
            {"numero1": -4, "numero2": 2, "resultado_esperado": -8},
            {"numero1": 4, "numero2": 2, "resultado_esperado": 2},
            {"numero1": -4, "numero2": 2, "resultado_esperado": -2}

        ]

    # ingresamos el  para que se vea que s epued eponer 2 fixtures en una mosma funcion
    @pytest.mark.smoke
    #se puede agregar mas de una categoria
    @pytest.mark.regression
    @pytest.mark.api

    def test_suma_numeros_positivos2(self, datos_numeros,setup_and_teardown):
        print("test")
        #setup
        a= datos_numeros[0]["numero1"]
        b= datos_numeros[0]["numero2"]
        resultado_esperado= datos_numeros[0]["resultado_esperado"]

        #ejecucion
        resultado_actual= self.op.suma(a,b)
        ##validacion

        assert resultado_actual == resultado_esperado,\
        f"Validando suma de numeros positovs. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)


    @pytest.mark.smoke
    @pytest.mark.regression
    #para ejeuctar los marcado podemos ejeuctar desde terminal como->
    #  pytest -m "regresion"
    def test_suma_numeros_negativos2(self, datos_numeros,setup_and_teardown):
        #self.test_suma_numeros_positivos2(datos_numeros) #sirve para llamar un test dentro de otro
        print("test")
        #setup
        a= datos_numeros[1]["numero1"]
        b= datos_numeros[1]["numero2"]
        resultado_esperado= datos_numeros[1]["resultado_esperado"]

        #ejecucion
        resultado_actual= self.op.suma(a,b)
        ##validacion

        assert resultado_actual == resultado_esperado,\
        f"Validando suma de numeros negativos. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    @pytest.mark.smoke
    def test_resta_numeros_positivos2(self,datos_numeros,setup_and_teardown):
        print("test")
        #setup
        a=datos_numeros[2]["numero1"]
        b=datos_numeros[2]["numero2"]
        resultado_esperado = datos_numeros[2]["resultado_esperado"]
        # ejecucion
        resultado_actual = self.op.resta(a, b)
        ##validacion

        assert resultado_actual == resultado_esperado, \
            f"Validando resta de numeros positivos. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    @pytest.mark.smoke
    def test_resta_numeros_negativos2(self,datos_numeros,setup_and_teardown):
        print("test")
        #setup
        a=datos_numeros[3]["numero1"]
        b=datos_numeros[3]["numero2"]
        resultado_esperado = datos_numeros[3]["resultado_esperado"]
        # ejecucion
        resultado_actual = self.op.resta(a, b)
        ##validacion

        assert resultado_actual == resultado_esperado, \
            f"Validando resta de numeros positivos. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    @pytest.mark.smoke
    def test_multiplicacion_numeros_positivos2(self, datos_numeros,setup_and_teardown):
        print("test")
        # setup
        a = datos_numeros[4]["numero1"]
        b = datos_numeros[4]["numero2"]
        resultado_esperado = datos_numeros[4]["resultado_esperado"]

        # ejecucion
        resultado_actual = self.op.multiplicacion(a, b)
        ##validacion

        assert resultado_actual == resultado_esperado, \
            f"Validando suma de numeros positovs. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    @pytest.mark.smoke
    def test_multiplicacion_numeros_negativo2(self, datos_numeros):
        print("test")
        # setup
        a = datos_numeros[5]["numero1"]
        b = datos_numeros[5]["numero2"]
        resultado_esperado = datos_numeros[5]["resultado_esperado"]

        # ejecucion
        resultado_actual = self.op.multiplicacion(a, b)
        ##validacion

        assert resultado_actual == resultado_esperado, \
            f"Validando suma de numeros positovs. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    @pytest.mark.smoke
    def test_division_numeros_positivos2(self, datos_numeros):
        print("test")
        # setup
        a = datos_numeros[6]["numero1"]
        b = datos_numeros[6]["numero2"]
        resultado_esperado = datos_numeros[6]["resultado_esperado"]

        # ejecucion
        resultado_actual = self.op.division(a, b)
        ##validacion

        assert resultado_actual == resultado_esperado, \
            f"Validando suma de numeros positovs. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    @pytest.mark.smoke
    def test_division_numeros_negativo2(self, datos_numeros):
        print("test")
        # setup
        a = datos_numeros[7]["numero1"]
        b = datos_numeros[7]["numero2"]
        resultado_esperado = datos_numeros[7]["resultado_esperado"]

        # ejecucion
        resultado_actual = self.op.division(a, b)
        ##validacion

        assert resultado_actual == resultado_esperado, \
            f"Validando suma de numeros positovs. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    ###

    def test_suma_numeros_positivos(self):
        print("test de la suma +")
        #setup
        a=3
        b=4
        resultado_esperado = 7

    #resultado = 2 + 3
    #assert resultado == 5
        #op = OperacionesMatematicas()
        ##ejecucion
        resultado_actual= self.op.suma(3,4)
        ##validacion
        #print("resultado:",resultado)
        assert resultado_actual == resultado_esperado,\
        f"Validando suma de numeros positivos. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_suma_numeros_negativos(self):
        print("test de la suma -")
        a= -3
        b=2
        resultado_esperado = -1
        # resultado = 2 + 3
        # assert resultado == 5
        # op = OperacionesMatematicas()
        resultado_actual = self.op.suma(-3, 2)
        #print("resultado:", resultado)
        assert resultado_actual == resultado_esperado, \
        f"Validando suma de numeros negativos.RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)


    def test_resta_numeros_positivos(self):
        print("test de la resta +")
        #setup
        a=6
        b=4
        resultado_esperado = 2

    #resultado = 2 + 3
    #assert resultado == 5
        #op = OperacionesMatematicas()
        ##ejecucion
        resultado_actual= self.op.resta(6,4)
        ##validacion
        #print("resultado:",resultado)
        assert resultado_actual == resultado_esperado, \
        f"Validando resta de numeros positivos.RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_resta_numeros_negativos(self):
        print("test de la resta -")
        a= 3
        b= 5
        resultado_esperado = -2
        # resultado = 2 + 3
        # assert resultado == 5
        # op = OperacionesMatematicas()
        resultado_actual = self.op.resta(3, 5)
        #print("resultado:", resultado)
        assert resultado_actual == resultado_esperado, \
        f"Validando resta de numeros negativos.RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_multiplicacion_numeros_positivos(self):
        print("test de la multiplicacion +")
        #setup
        a=6
        b=4
        resultado_esperado = 24

    #resultado = 2 + 3
    #assert resultado == 5
        #op = OperacionesMatematicas()
        ##ejecucion
        resultado_actual= self.op.multiplicacion(6,4)
        ##validacion
        #print("resultado:",resultado)
        assert resultado_actual == resultado_esperado, \
        f"Validando multiplicacion de numeros positivos.RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_multiplicacion_numeros_negativos(self):
        print("test de la multiplicacion -")
        a= 3
        b=-5
        resultado_esperado = -15
        # resultado = 2 + 3
        # assert resultado == 5
        # op = OperacionesMatematicas()
        resultado_actual = self.op.multiplicacion(3, -5)
        #print("resultado:", resultado)
        assert resultado_actual == resultado_esperado,\
        f"Validando multiplicacion de numeros negativos.RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_division_numeros_positivos(self):
        print("test de la division +")
        #setup
        a=6
        b=2
        resultado_esperado = 3

    #resultado = 2 + 3
    #assert resultado == 5
        #op = OperacionesMatematicas()
        ##ejecucion
        resultado_actual= self.op.division(6,2)
        ##validacion
        #print("resultado:",resultado)
        assert resultado_actual == resultado_esperado, \
        f"validando division de numeros positivos.RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_division_numeros_negativos(self):
        print("test de la dividion -")
        a= 15
        b=-5
        resultado_esperado = -3
        # resultado = 2 + 3
        # assert resultado == 5
        # op = OperacionesMatematicas()
        resultado_actual = self.op.division(15, -5)
        #print("resultado:", resultado)
        assert resultado_actual == resultado_esperado, \
        f"Validando resta de numeros positivos.RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_compara_letra(self):
        letra = "hoLa"
        letra2 = "Hola"

        assert letra.lower() == letra2.lower(), "validando letra esperado"
        #lower para convertir las letras iguales

    def test_compara_letra2(self):
        ra = " Hola"
        re = "Hola "

        assert ra.strip() == re.strip() , "validando letras quitando espacios al inicio y final"
        #strip para quitar los espacios al inicio y al final

    def test_compara_letra3(self):
        ra = "Hola Hola"
        re = "HolaHola"
        ra = ra.replace(" ", "")

        assert ra.strip() == re, "validando letras quitando espacios dentro del txto"
        # strip para quitar los espacios al inicio y al final

    def test_mayor_positivos(self):
        print("test mayor +")
        #setup
        a=3
        b=4
        resultado_esperado = 7

    #resultado = 2 + 3
    #assert resultado == 5
        #op = OperacionesMatematicas()
        ##ejecucion
        resultado_actual= self.op.suma(3,9)
        ##validacion
        #print("resultado:",resultado)
        assert resultado_actual > resultado_esperado
        f"Validando suma de numeros positivos. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_menor_positivos(self):
        print("test menor +")
        #setup
        a=3
        b=4
        resultado_esperado = 15

    #resultado = 2 + 3
    #assert resultado == 5
        #op = OperacionesMatematicas()
        ##ejecucion
        resultado_actual= self.op.suma(3,9)
        ##validacion
        #print("resultado:",resultado)
        assert resultado_actual < resultado_esperado
        f"Validando suma de numeros positivos. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)

    def test_difrente_positivos(self):
        print("test diferente +")
        #setup
        a=3
        b=4
        resultado_esperado = 15

    #resultado = 2 + 3
    #assert resultado == 5
        #op = OperacionesMatematicas()
        ##ejecucion
        resultado_actual= self.op.suma(3,9)
        ##validacion
        #print("resultado:",resultado)
        assert resultado_actual != resultado_esperado
        f"Validando suma de numeros positivos. RA:{resultado_actual}. RE:{resultado_esperado}"
        print("resultado:", resultado_actual)
    def test_verificar_numero_par(self):
        objeto = OperacionesMatematicas()
        # Esto llamará a la función 'par' ejecutando la línea faltante
        assert objeto.par(4) is True  # Cambia a False si decidiste dejar el código original con == 1
