import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parámetros
m = 10.0  # kg
g = 9.81  # m/s^2

def F_c(t):
    return m * g  # Compensa gravedad

def F_ext(t):
    return 5.0 * np.sin(0.5 * t)  # Fuerza externa oscilatoria

# Ecuación diferencial: [z, z_dot]
def dynamics(t, y):
    z, zdot = y
    acc = (-m * g + F_c(t) + F_ext(t)) / m
    return [zdot, acc]

# Condiciones iniciales
y0 = [0.0, 0.0]  # z=0, z_dot=0

# Tiempo de simulación
t_span = (0, 20)
t_eval = np.linspace(*t_span, 500)

# Resolver
sol = solve_ivp(dynamics, t_span, y0, t_eval=t_eval)

# Graficar
plt.plot(sol.t, sol.y[0])
plt.title("Posición vertical de la masa (sistema gravedad cero)")
plt.xlabel("Tiempo [s]")
plt.ylabel("z [m]")
plt.grid()
plt.show()
