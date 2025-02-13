

# Pedir un número al usuario  
x = int(input("Introduce tu numero: "))  # Convertir a entero  

def sqrt(x):  
    """Returns the square root of x, if x is a perfect square.  
    Prints an error message and returns None otherwise"""  
    ans = 0  
    if x >= 0:  
        while ans * ans < x:  
            ans += 1  
        if ans * ans != x:  
            print(x, 'is not a perfect square')  
            return None  
        else:  
            return ans  
    else:  
        print(x, 'is a negative number')  
        return None  

def f(x):  
    x = x + 1  
    return x  

# Usando las funciones  
resultado_sqrt = sqrt(x)  
if resultado_sqrt is not None:  
    print("La raíz cuadrada de", x, "es", resultado_sqrt)  

resultado_f = f(x)  
print("El resultado de f(x) es", resultado_f)

