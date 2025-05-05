import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import StateSpace, lti, step

# Función para calcular la masa del cilindro ISO 15552
def get_cylinder_mass(diameter_mm, stroke_mm):
    masses_1000 = {32:2.2,40:3.0,50:4.5,63:6.5,80:10.5,100:15.0,125:20.0,160:28.0}
    if diameter_mm not in masses_1000:
        raise ValueError("Diámetro no soportado.")
    return masses_1000[diameter_mm] * (stroke_mm/1000.0)

# Parámetros del sistema
m_carga = 10.0      # kg
diametro = 63       # mm
carrera = 800       # mm
m_cilindro = get_cylinder_mass(diametro, carrera)
m_total = m_carga + m_cilindro

g = 9.81  # gravedad (m/s^2)

# Dinámica del sistema (gravedad cero compensada)
def F_c(t):
    return m_total * g

def F_ext(t):
    return 5.0 * np.sin(0.5 * t)

def dynamics(t, y):
    z, zdot = y
    acc = (-m_total * g + F_c(t) + F_ext(t)) / m_total
    return [zdot, acc]

# Simulación temporal con solve_ivp
y0 = [0.0, 0.0]  # condición inicial: z=0, velocidad=0
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 500)
sol = solve_ivp(dynamics, t_span, y0, t_eval=t_eval)

# Diseño de LQR aproximado sin el paquete 'control'
# Modelo: doble integrador
A = np.array([[0, 1], [0, 0]])
B = np.array([[0], [1/m_total]])
C = np.array([[1, 0]])
D = np.array([[0]])

# Parámetros de costo
Q = np.diag([100, 1])
R = np.array([[1]])

# Resolución algebraica de Riccati para obtener LQR
from scipy.linalg import solve_continuous_are

P = solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P
Acl = A - B @ K

# Verificación de estabilidad del lazo cerrado
eigvals = np.linalg.eigvals(Acl)
print("Polos del lazo cerrado:", eigvals)
if not np.all(np.real(eigvals) < 0):
    raise RuntimeError("El sistema en lazo cerrado no es estable!")

# Simulación del sistema en lazo cerrado
sys_cl = StateSpace(Acl, B, C, D)
t_lqr = np.linspace(0, 5, 200)
t_out, y_lqr, _ = lti(Acl, B, C, D).output(U=np.ones_like(t_lqr), T=t_lqr)

# Graficar resultados
t = sol.t
nz = sol.y[0]
vz = sol.y[1]

plt.figure(figsize=(10, 8))

plt.subplot(3,1,1)
plt.plot(t, nz, label='Posición (sim)')
plt.title('Dinámica y respuesta LQR')
plt.ylabel('z [m]')
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(t, vz, label='Velocidad (sim)', color='orange')
plt.ylabel('v [m/s]')
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(t_out, y_lqr, label='LQR Step', color='green')
plt.ylabel('z [m]')
plt.xlabel('Tiempo [s]')
plt.grid(True)

plt.tight_layout()
plt.show()
