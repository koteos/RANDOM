import numpy as np  
import matplotlib.pyplot as plt  

# Datos de entrada (horas de estudio) y salida (calificaciones)  
X = np.array([1, 2, 3, 4, 5])  # Horas de estudio  
y = np.array([0.8, 3, 7, 8.5, 13])  # Calificaciones  

# Inicialización de parámetros (pesos y sesgo)  
w = 2.16  # Peso  
b = -0.74  # Sesgo  
learning_rate = 0.01  # Tasa de aprendizaje  
epochs = 1000  # Número de iteraciones  

# Función de pérdida (Error cuadrático medio)  
def calculate_loss(X, y, w, b):  
    total_loss = 0  
    n = len(y)  
    for i in range(n):  
        y_pred = w * X[i] + b  # Predicción  
        total_loss += (y[i] - y_pred) ** 2  # Error  
    return total_loss / n  # MSE  

# Entrenamiento del modelo  
for epoch in range(epochs):  
    # Actualización de pesos y sesgo  
    for i in range(len(y)):  
        y_pred = w * X[i] + b  # Predicción  
        error = y[i] - y_pred  # Cálculo del error  
        
        # Gradientes  
        w_gradient = -2 * X[i] * error  # Gradiente del peso  
        b_gradient = -2 * error          # Gradiente del sesgo  

        # Actualizando pesos y sesgo  
        w -= learning_rate * w_gradient  
        b -= learning_rate * b_gradient  

    # Mostrar la pérdida cada 10 iteraciones  
    if epoch % 10 == 0:  
        loss = calculate_loss(X, y, w, b)  
        print(f"Epoch {epoch}, Loss: {loss}, w: {w}, b: {b}")  

# Visualizar resultados  
plt.scatter(X, y, color='blue', label='Datos Reales')  
plt.plot(X, w * X + b, color='red', label='Modelo Aprendido')  
plt.xlabel('Horas de Estudio')  
plt.ylabel('Calificación')  
plt.title('Regresión Lineal Simple')  
plt.legend()  
plt.show()
