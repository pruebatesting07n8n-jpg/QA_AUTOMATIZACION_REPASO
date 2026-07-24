##Para instalar pip install + nombre del paquete
#Variable= valor
#usar letras y numeros, no usar espacio o iniciar con digitos, unas minus y palabras en ingles
#ejemplo nombre = "Anali"
#si no las llamamos no funciona
# sirve para imprrimir -> print
#Tipos de datos= enteros, numeros reales, strings, booleanos(true/false)
#-> lista, diccionarios, coleccion ordenada pares
#Estructuras de control condicionales(if/else) bucles(for/ while)


edad =20
##Condicionaes
if edad > 18:
    print("Mayor de edad")
else:
    print("menor de edad")

##Bucles
for i in range(5):
    print(i)

##funciones -> acciones que va a realizar mi script
# def + nombre de la funcion +():
#Para llamarlas se tiene que poner argumentos o parametros de entrada
def saludo():
    instructor = "May"
    alumno = "Ronald"

    print("Hola, "+alumno+ ". Tu instructor es "+instructor)
saludo()


def saludo2(alumno, instructor):

    print("Hola, " + alumno + ". Tu instructor es " + instructor)
saludo2("Pablo", "Ronald")

