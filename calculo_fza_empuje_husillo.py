import math

# Pedir el torque en Nm
torque = float(input("Ingresa el torque en Nm:  ",))
# Pedir el paso en mm
paso = float (input("Ingresa el paso en mm:  ",))
# Pedir la eficiencia del husillo 
efi = float (input("Ingresa la eficiencia en %:  "))

#vamos a convertir el paso a metros 
paso = paso / 1000

# convertimos eficiencia en flotante 
efi = efi / 100

#Calculmaos el empuje
empuje = (2 * math.pi * torque * efi) / paso

# calculamos en kilogramos 
empuje_kg = empuje / 9.8

# Mostramos el resultado
print (f"La fuerza de empuje en Newtons es: {empuje: .2f}")
print (f"La fuerza de empuje en Kilos es: {empuje_kg: .2f}")