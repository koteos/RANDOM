import math

def calcular_fuerza_avance(torque_entrada, eficiencia_husillo, paso_husillo):
    fuerza_avance = (2 * math.pi * eficiencia_husillo * torque_entrada) / paso_husillo
    return fuerza_avance

def main():
    print("Calculadora de Fuerza de Avance para Tornillo Sin Fin")
    while True:
        torque_entrada = float(input("Ingrese el torque de entrada (Nmm): "))
        eficiencia_husillo = float(input("Ingrese la eficiencia del husillo (porcentaje): ")) / 100
        paso_husillo = float(input("Ingrese el paso del husillo (mm): "))

        fuerza_avance = calcular_fuerza_avance(torque_entrada, eficiencia_husillo, paso_husillo)
        print("La fuerza de avance del tornillo sin fin es:", fuerza_avance, "N")

        respuesta = input("¿Desea calcular nuevamente? (s/n): ")
        if respuesta.lower() != "s":
            break

if __name__ == "__main__":
    main()
