import numpy as np
import control as ctrl

# Rango de masas
masses = np.linspace(5, 100, 20)      # 10 puntos entre 5 y 50 kg
data = []
for m in masses:
    A = np.array([[0,1],[0,0]])
    B = np.array([[0],[1/m]])
    Q = np.diag([100,50])
    R = np.array([[1]])
    K,_,_ = ctrl.lqr(A, B, Q, R)
    data.append((m, float(K[0,0]), float(K[0,1])))

for m,K1,K2 in data:
    print(f"  {{ {m:.1f}f, {K1:.4f}f, {K2:.4f}f }},")
