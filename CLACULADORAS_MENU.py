import math

# Voy a definir el menú principal. Recuerda que con DEF defines una etiqueta con su algoritmo y después puedes llamarla.  
def menu():  # Aquí definimos la variable y abajo ponemos el algoritmo a ejecutar  
    print("¿Qué deseas calcular?")  # Menú  
    print("1. Calculadora Fuerza de Husillo")  # case 1  
    print("2. Calculadora Torque motor")  # case 2  
    print("3. Calculadora Viga en Voladizo")  # case 3  
    print("4. Calculadora Viga Doble Empotrada")  # case 4  

def calculadora1():  
    # Pedir el torque en Nm
    torque = float(input("Ingresa el torque en Nm:  ",))
    # Pedir el paso en mm
    paso = float (input("Ingresa el paso en mm:  ",))
    # Pedir la eficiencia del husillo 
    efi = float (input("Ingresa la eficiencia en %:  "))

    #vamos a convertir el paso a metros 
    paso = paso / 1000

    # convertimos eficiencia en flotante 
    efi = efi / 100

    #Calculmaos el empuje
    empuje = (2 * math.pi * torque * efi) / paso

    # calculamos en kilogramos 
    empuje_kg = empuje / 9.8

    # Mostramos el resultado
    print (f"La fuerza de empuje en Newtons es: {empuje: .2f}")
    print (f"La fuerza de empuje en Kilos es: {empuje_kg: .2f}")


def calculadora2():
    Potencia = 0.0
    Torque = 0.0
    RPM = 0
    print("¿Qué deseas calcular?, Recuerda que P = T · π · RPM / 30")  # 
    print("1. Tengo RPM y Par, calcular Potencia en Watts")  # case 1  
    print("2. Tengo RPM y Potencia, calcular Torque en Nm")  # case 2  
    print("3. Tengo Potencia y Par, calcular RPM")  # case 3
    seleccion = int(input("Selecciona una opción: "))

    
    match seleccion:  
        case 1:
            # Pedir el torque en Nm
            Torque = float(input("Ingresa el torque en Nm: "))
            # Pedir las RPM
            RPM = int(input("Ingresa las RPM:  ",))
            Potencia = (Torque * math.pi * RPM)/30
            print(f"La potencia en Watt es: {Potencia:.2f}")
            
        case 2:  
            # Pedir la Potencia en Watts
            Potencia = float(input("Ingresa la Potencia en Watts:  ",))
            # Pedir las RPM
            RPM = int(input("Ingresa las RPM:  ",))
            Torque = (30 * Potencia) / (math.pi * RPM)
            print(f"El Torque en Nm es: {Torque:.2f}")
            
        case 3:  
            # Pedir la Potencia en Watts
            Potencia = float(input("Ingresa la Potencia en Watts:  ",))
            # Pedir el Torque
            Torque = float(input("Ingresa el Torque en Nm:  ",))
            RPM = (30 * Potencia)/ (math.pi * Torque)
            print(f"Las RPM son: {RPM:.2f}")
            
        case _:  
            print("Opción no válida")
            
def calculadora3():  
    # Aquí debo colocar el algoritmo del cálculo, pero es una prueba así que solo voy a imprimir algo  
    print("Cálculo de viga en voladizo")  

def calculadora4():  
    # Aquí debo colocar el algoritmo del cálculo, pero es una prueba así que solo voy a imprimir algo  
    print("Cálculo de viga doble empotrada")  

def switch_example(seleccion):  
    match seleccion:  
        case 1:  
            calculadora1()  
        case 2:  
            calculadora2()   
        case 3:  
            calculadora3()   
        case 4:  
            calculadora4()  
        case _:  
            print("Opción no válida")  

while True:  # Ciclo que repetirá el menú hasta que se elija salir  
    menu()  
    seleccion = int(input("Selecciona una opción: "))  # Solicitar selección  

    switch_example(seleccion)  # Llamar la función según la selección  

    respuesta = input("¿Deseas hacer otro cálculo? (si/no): ").strip().lower()  # Pregunta si desea continuar  
    if respuesta != "si":  
        print("Hecho. ¡Hasta luego!")  
        break  # Salir del bucle if la respuesta no es "si"
