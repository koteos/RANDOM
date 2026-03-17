import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def plot_resortF(L0=270.0, Lf=373.16, k=0.7539):
    if Lf <= L0:
        print("Lf debe ser mayor que L0.")
        return

    xf = Lf - L0
    F_final = k * xf

    # Curva F(L) = k * (L - L0) para L en [L0, Lf]
    num_puntos = 300
    L = np.linspace(L0, Lf, num_puntos)
    F = k * (L - L0)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(L, F, color='tab:blue', label='Fuerza en función de la longitud')
    ax.set_title('Fuerza vs Longitud del resorte')
    ax.set_xlabel('Longitud del resorte (mm)')
    ax.set_ylabel('Fuerza (DaN)')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    annotation = ax.annotate('', xy=(0,0), xytext=(15,-15),
                           textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
                           arrowprops=dict(arrowstyle='->'))
    annotation.set_visible(False)

    def on_move(event):
        if event.inaxes != ax:
            annotation.set_visible(False)
            fig.canvas.draw_idle()
            return
        xdata = event.xdata
        if xdata < L0 or xdata > Lf:
            annotation.set_visible(False)
            fig.canvas.draw_idle()
            return
        F_cur = k * (xdata - L0)
        annotation.xy = (xdata, F_cur)
        annotation.set_text(f"L = {xdata:.2f} mm\nF = {F_cur:.3f} DaN")
        annotation.set_visible(True)
        fig.canvas.draw_idle()

    cid = fig.canvas.mpl_connect('motion_notify_event', on_move)
    plt.show()

# Interactivos
interact(
    plot_resortF,
    L0=FloatSlider(min=100, max=1000, step=1, value=290.0, description='L0 (mm)'),
    Lf=FloatSlider(min=100.1, max=1200, step=1, value=402.53, description='Lf (mm)'),
    k=FloatSlider(min=0.1, max=5.0, step=0.01, value=0.6911, description='k (DaN/mm)')
)
