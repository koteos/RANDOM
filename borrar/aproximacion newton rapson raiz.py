def newton_raphson_sqrt(value, initial_guess=1.0, tolerance=1e-7, max_iterations=1000):  
    x_n = initial_guess  # Valor inicial  
    f = lambda x: x**2 - value  # Función  
    f_prime = lambda x: 2 * x  # Derivada de la función  

    for iteration in range(max_iterations):  
        # Cálculo de la función y su derivada  
        f_x_n = f(x_n)  
        f_prime_x_n = f_prime(x_n)  

        # Comprobar si la derivada es cero  
        if f_prime_x_n == 0:  
            raise ValueError("La derivada se volvió cero. Método no puede continuar.")  
        
        # Calcular el siguiente valor  
        x_n1 = x_n - f_x_n / f_prime_x_n  
        
        # Comprobar la convergencia  
        if abs(x_n1 - x_n) < tolerance:  
            return x_n1  # Retornar la raíz encontrada  
        
        x_n = x_n1  

    return x_n  # Retornar el último valor si no se alcanzó la convergencia  

# Solicitar al usuario que ingrese el valor del cual quiere calcular la raíz  
value_to_sqrt = float(input("Introduce el número del cual deseas calcular la raíz cuadrada: "))  
decimal_precision = int(input("Introduce la precisión deseada en decimales: "))  

# Establecer la tolerancia en función de la precisión deseada  
tolerance = 10**(-decimal_precision)  

# Usar la función para calcular la raíz cuadrada del valor ingresado  
root = newton_raphson_sqrt(value_to_sqrt, tolerance=tolerance)  

# Imprimir el resultado con la precisión deseada  
print(f"La raíz cuadrada de {value_to_sqrt} es aproximadamente: {root:.{decimal_precision}f}")
