import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def get_cylinder_mass(diameter_mm, stroke_mm):
    # Masa estimada en kg para carrera de 1000 mm
    masses_1000 = {
        32: 2.2,
        40: 3.0,
        50: 4.5,
        63: 6.5,
        80: 10.5,
        100: 15.0,
        125: 20.0,
        160: 28.0
    }
    if diameter_mm not in masses_1000:
        raise ValueError("Diámetro no soportado.")
    base_mass = masses_1000[diameter_mm]
    return base_mass * (stroke_mm / 1000.0)

# Parámetros
m_carga = 10.0     # kg
diametro = 63      # mm
carrera = 800      # mm
m_cilindro = get_cylinder_mass(diametro, carrera)
m_total = m_carga + m_cilindro
g = 9.81

# Fuerza del cilindro (compensación de gravedad)
def F_c(t):
    return m_total * g

# Perturbación externa: fuerza senoidal
def F_ext(t):
    return 5.0 * np.sin(0.5 * t)

# Ecuaciones del sistema
def dynamics(t, y):
    z, zdot = y
    acc = (-m_total * g + F_c(t) + F_ext(t)) / m_total
    return [zdot, acc]

# Condiciones iniciales: posición y velocidad inicial
y0 = [0.0, 0.0]
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 500)

# Resolver la dinámica
sol = solve_ivp(dynamics, t_span, y0, t_eval=t_eval)

# Graficar resultados
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(sol.t, sol.y[0])
plt.title("Posición y velocidad vs. tiempo")
plt.ylabel("Posición (m)")
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(sol.t, sol.y[1])
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad (m/s)")
plt.grid()
plt.tight_layout()
plt.show()

import control as ctrl
import matplotlib.pyplot as plt

# Parámetros
m_carga = 10.0       # kg
m_cilindro = get_cylinder_mass(63, 800)  # reutiliza tu función
m_total = m_carga + m_cilindro

# Definir función de transferencia G(s)=1/(m_total * s^2)
num = [1.0]
den = [m_total, 0.0, 0.0]
G = ctrl.TransferFunction(num, den)

# Mostrar pólos y ceros
print("G(s) =", G)
print("Ceros:", ctrl.zero(G))
print("Polos:", ctrl.pole(G))

# Respuesta al escalón
t, y = ctrl.step_response(G)
plt.figure()
plt.plot(t, y)
plt.title('Respuesta al escalón de G(s)')
plt.xlabel('Tiempo [s]')
plt.ylabel('Posición [m] ante 1 N')
plt.grid()
plt.show()

