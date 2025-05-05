import numpy as np
import control as ctrl

# Parámetros
m_total = 15.2  # kg

# Matrices del sistema
A = np.array([[0, 1],
              [0, 0]])
B = np.array([[0],
              [1/m_total]])

# Pesos LQR
Q = np.diag([100, 1])
R = np.array([[1]])

# Cálculo de K
K, S, E = ctrl.lqr(A, B, Q, R)

print("Ganancia K:", K)
print("Valores propios del lazo cerrado:", E)

import matplotlib.pyplot as plt

# Sistema de lazo cerrado
Acl = A - B @ K
sys_cl = ctrl.ss(Acl, B, np.eye(2), np.zeros((2,1)))

# Respuesta al escalón en posición
t, y = ctrl.step_response(sys_cl[0], T=np.linspace(0,5,200))

plt.plot(t, y)
plt.title("Respuesta al escalón en posición con LQR")
plt.xlabel("Tiempo [s]")
plt.ylabel("z [m]")
plt.grid()
plt.show()
