import matplotlib.pyplot as plt  

def fibonacci(n):  
    """Genera una lista de los primeros n números de la secuencia de Fibonacci."""  
    fib_sequence = [0, 1]  
    for i in range(2, n):  
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])  
    return fib_sequence[:n]  

def graficar_fibonacci(n):  
    """Grafica la secuencia de Fibonacci."""  
    if n <= 0:  
        print("Por favor, ingresa un número mayor que 0.")  
        return  

    fib_sequence = fibonacci(n)  
    plt.figure(figsize=(10, 5))  
    plt.plot(fib_sequence, marker='o')  
    plt.title(f'Secuencia de Fibonacci ({n} números)')  
    plt.xlabel('Índice')  
    plt.ylabel('Valor')  
    plt.xticks(range(n))  
    plt.grid()  
    plt.show()  

# Solicitar al usuario la longitud de la secuencia  
try:  
    longitud = int(input("Ingrese la longitud de la secuencia de Fibonacci que desea graficar: "))  
    graficar_fibonacci(longitud)  
except ValueError:  
    print("Por favor, ingrese un número entero válido.")
