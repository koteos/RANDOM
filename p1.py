while True:


    # Solicitar la altura del rectangulo

    print( "CALCULO DEL AREA DE UN RECTANGULO" )

    base = float (input ("Ingresa la base del rectangulo:"))
    altura = float (input ("introduce el valor de la altura:"))

    # Sección donde se calcula el área
    area = (base * altura)

    # Vamos a mostrar el valor de la ecuacion
    print("area del reactangulo es:" , area)


    # Preguntar al ususario si quiere repetir
    respuesta = input("Deseas volver a calcular otra area? (s/n): ")

    # Si la respuesta es no que salga del bucle
    if respuesta.lower() != "s":
        break
