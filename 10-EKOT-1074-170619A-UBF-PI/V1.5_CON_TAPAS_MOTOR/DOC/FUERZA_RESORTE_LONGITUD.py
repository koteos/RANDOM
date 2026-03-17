import numpy as np
import matplotlib.pyplot as plt

# Datos proporcionados
L0 = 290.0        # Longitud en reposo del resorte (mm)
Lf = 402.53        # Longitud total extendida (mm)
k = 0.6911          # DaN/mm (constante del resorte)

# Verificación de consistencia
xf = Lf - L0  # elongación final desde reposo
F_final = k * xf  # Fuerza final esperada (DaN)

print(f"Longitud en reposo L0: {L0:.3f} mm")
print(f"Longitud final Lf: {Lf:.3f} mm")
print(f"Elongación final xf: {xf:.3f} mm")
print(f"Fuerza final F = k * x: {F_final:.4f} DaN")

# Crear un vector de longitudes desde L0 hasta Lf
num_puntos = 200
L = np.linspace(L0, Lf, num_puntos)

# Calcular la fuerza para cada longitud: F = k * (L - L0)
F = k * (L - L0)

# Graficar: Fuerza vs Longitud
plt.figure(figsize=(8, 4))
plt.plot(L, F, label='Fuerza en función de la longitud', color='tab:blue')
plt.title('Fuerza vs Longitud del resorte')
plt.xlabel('Longitud del resorte (mm)')
plt.ylabel('Fuerza (DaN)')
plt.grid(True, linestyle='--', alpha=0.6)

# Marcar longitud final y recompensa visual
plt.axvline(x=Lf, color='tab:orange', linestyle='--', label='Longitud final (Lf)')
plt.legend()
plt.tight_layout()
plt.show()
