

#Voy a definir el menu principal, recuerda que con DEF defines una etiqueta con su algoritmo y despues puedes llamarla
def menu(): #aqui definimos la variable y abajo ponemos el algoritmo a ejecutar
    print("¿Qué deseas calcular?")
    print("1. Calculadora Fuerza de Husillo")
    print("2. Calculadora viga en voladizo")
    print("3. Calculadora viga 2ble empotrada")

    opcion = int(input("¿Qué deseas calcular?"))
    if opcion == 1:
        calculadora1()
    elif opcion == 2:
        calculadora2()
    elif opcion == 3:
        calculadora3()
    else:
        print("Opcion no valida")

def calculadora1():
    # aqui debo colocar el algoritmo del calculo, pero es una prueba asi que solo voy a imprimir algo
    print("Cálculo fuerza de husillo")

def calculadora2():
    #aqui debo colocar el algoritmo del calculo, pero es una prueba asi que solo voy a imprimir algo
    print("Cálculo de viga en voladizo")

def calculadora3():
    #aqui debo colocar el algoritmo del calculo, pero es una prueba asi que solo voy a imprimir algo
    print("Cálculo de viga 2ble empotrada")




respuesta = int(input("¿deseas hacer otro cálculo?"))
if respuesta == "si":
                menu()

else :
    print("hecho")


