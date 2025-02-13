import numpy as np  
import matplotlib.pyplot as plt  

# Datos de entrada (horas de estudio) y salida (calificaciones)  
X = np.array([1, 2, 3, 4, 5])  # Horas de estudio  
y = np.array([1, 4.5, 6.3, 9, 10])  # Calificaciones  

# Inicialización de parámetros (pesos y sesgo)  
w = 0.0  # Peso  
b = 0.0  # Sesgo  
learning_rate = 0.01  # Tasa de aprendizaje  
epochs = 100  # Número de iteraciones  

# Entrenamiento del modelo  
for epoch in range(epochs):  
    for i in range(len(y)):  
        y_pred = w * X[i] + b  # Predicción  
        error = y[i] - y_pred  # Cálculo del error  
        
        # Gradientes  
        w_gradient = -2 * X[i] * error  # Gradiente del peso  
        b_gradient = -2 * error          # Gradiente del sesgo  

        # Actualizando pesos y sesgo  
        w -= learning_rate * w_gradient  
        b -= learning_rate * b_gradient  

# Función para predecir la calificación basada en horas de estudio  
def predict(hours_studied):
   
    return w * hours_studied + b  

# Interacción con el usuario  
while True:
    print("valor w: ", w, "\n", "valor b: ", b)
    try:  
        input_hours = float(input("Introduce las horas de estudio (o escribe 'e' para salir): "))  
        predicted_grade = predict(input_hours)  
        print(f"Predicción de calificación para {input_hours} horas de estudio: {predicted_grade:.2f}")  
    except ValueError:  
        print("¡Salida! Si necesitas hacer otra predicción, reinicia el programa.")  
        break  

# Opcional: Visualizar los resultados  
plt.scatter(X, y, color='blue', label='Datos Reales')  
plt.plot(X, w * X + b, color='red', label='Modelo Aprendido')  
plt.xlabel('Horas de Estudio')  
plt.ylabel('Calificación')  
plt.title('Predicción de Calificaciones')  
plt.legend()  
plt.show()
