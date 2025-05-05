import numpy as np
import control as ctrl

# Diccionario con masas por 1000 mm de carrera (en kg)
MASAS_CILINDROS_ISO15552 = {
    32: 2.2,
    40: 3.0,
    50: 4.5,
    63: 6.5,
    80: 10.5,
    100: 15.0,
    125: 20.0,
    160: 28.0
}

def get_cylinder_mass(diameter_mm, stroke_mm):
    if diameter_mm not in MASAS_CILINDROS_ISO15552:
        raise ValueError(f"Diámetro {diameter_mm} mm no soportado. Usa uno de estos: {list(MASAS_CILINDROS_ISO15552.keys())}")
    masa_por_metro = MASAS_CILINDROS_ISO15552[diameter_mm]
    return masa_por_metro * (stroke_mm / 1000.0)

def calcular_lqr_gains(m_carga, diametro, carrera):
    m_cilindro = get_cylinder_mass(diametro, carrera)
    m_total = m_cilindro + m_carga

    A = np.array([[0, 1], [0, 0]])
    B = np.array([[0], [1 / m_total]])

    Q = np.diag([100, 1])  # Penaliza posición y velocidad
    R = np.array([[1]])    # Penaliza el esfuerzo de control

    K, _, _ = ctrl.lqr(A, B, Q, R)

    return {
        "m_total": m_total,
        "K1": float(K[0, 0]),
        "K2": float(K[0, 1])
    }

# === Interfaz interactiva con ciclo ===
if __name__ == "__main__":
    while True:
        try:
            print("\n--- Cálculo de Ganancias LQR ---")
            diametro = int(input("Ingresa el diámetro del cilindro (mm): "))
            carrera = float(input("Ingresa la carrera del cilindro (mm): "))
            m_carga = float(input("Ingresa la masa a cargar (kg): "))

            resultado = calcular_lqr_gains(m_carga, diametro, carrera)

            print("\n--- Resultados ---")
            print(f"Masa total (cilindro + carga): {resultado['m_total']:.2f} kg")
            print(f"K1 (posición): {resultado['K1']:.2f}")
            print(f"K2 (velocidad): {resultado['K2']:.2f}")

        except ValueError as e:
            print(f"Error: {e}")

        # Preguntar si desea repetir
        repetir = input("\n¿Deseas realizar otro cálculo? (SI / NO): ").strip().upper()
        if repetir != "SI":
            print("Saliendo del programa.")
            break
