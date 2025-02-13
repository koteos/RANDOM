
import math

while True:


def calcular_fuerza_avance(torque_entrada, eficiencia_husillo, paso_husillo):
    fuerza_avance = (2 * math.pi * eficiencia_husillo * torque_entrada) / paso_husillo
    return fuerza_avance

def main():
    print("Calculadora de Fuerza de Avance para Tornillo Sin Fin")
    torque_entrada = float(input("Ingrese el torque de entrada (Nmm): "))
    eficiencia_husillo = float(input("Ingrese la eficiencia del husillo (porcentaje): ")) / 100
    paso_husillo = float(input("Ingrese el paso del husillo (mm): "))

    fuerza_avance = calcular_fuerza_avance(torque_entrada, eficiencia_husillo, paso_husillo)
    print("La fuerza de avance del tornillo sin fin es:", fuerza_avance, "N")

if __name__ == "__main__":
    main()

   # Preguntar al usuario si desea realizar otra conversión
    respuesta = input("¿Desea realizar otra conversión? (s/n): ")

    # Si la respuesta no es "s", salir del bucle
    if respuesta.lower() != "s":
        break
