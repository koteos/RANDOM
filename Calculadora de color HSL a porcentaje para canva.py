
# Pedir un número al usuario  
print("Conversión HSL numérico a porcentaje % para Canva")  
m = int(input("Introduce matiz: "))  # Guardamos el dato en numérico de matiz  
s = int(input("Introduce saturación: "))  # Guardamos el dato en numérico de saturación  
l = int(input("Introduce brillo: "))  # Guardamos el dato en numérico de brillo  

Const = 255  # No necesitas especificar el tipo de la variable  

# Convertir a porcentaje  
m = int (m / Const * 1000)  
s = int (s / Const * 100)  
l = int (l / Const * 100)  

# Imprimir resultados con un salto de línea  
print("MATIZ     : ", m, "%")  # Imprime el matiz  
print("SATURACION: ", s, "%")  # Imprime la saturación  
print("BRILLO    :", l, "%")  # Imprime el brillo

