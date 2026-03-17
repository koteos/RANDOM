import numpy as np
import matplotlib.pyplot as plt

# Datos proporcionados
k = 0.6911  # DaN/mm
x0 = 0.0    # carrera inicial en mm
xf = 112.53  # carrera final en mm

# Verificación opcional: fuerza en x=xf esperada por F = k*x
F_expected = k * xf
print(f"Fuerza esperada en la carrera final (F = k * x): {F_expected:.4f} DaN")

# Crear un vector de carreras desde 0 hasta 112.53 mm (incluido)
# Puedes ajustar el número de puntos para mayor suavidad
num_puntos = 200
x = np.linspace(x0, xf, num_puntos)

# Calcular la fuerza usando la ley de Hooke: F = k * x
F = k * x  # DaN

# Opcional: si quieres mostrar la fuerza en kgf (1 DaN ≈ 0.10197 kgf)
# kgf = F * 0.101971621
# F_kgf = kgf

# Graficar
plt.figure(figsize=(8, 4))
plt.plot(x, F, label='Fuerza del resorte', color='tab:blue')
plt.title('Fuerza del resorte en función de la carrera')
plt.xlabel('Carrera (mm)')
plt.ylabel('Fuerza (DaN)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
