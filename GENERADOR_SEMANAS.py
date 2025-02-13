contador = int(input("Ingrese el valor del contador: "))
coordenada = input("Ingrese la coordenada: ").upper()
resultado = []

for i in range(contador):
    valor = f"'{32 + i}'!{coordenada}"
    resultado.append(valor)

cadena_resultante = '+'.join(resultado)
print(cadena_resultante)
