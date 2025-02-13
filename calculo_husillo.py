import math

# Pedir el torque en Nm
torque = float(input("Ingresa el torque en Nm:  ",))
# Pedir el paso en mm
paso = float (input("Ingresa el paso en mm:  ",))

#vamos a convertir el paso a metros 
paso = paso / 1000

#Calculmaos el empuje
empuje = (2 * math.pi * torque) / paso


# Mostramos el resultado
print (f"La fuerza de empuje en Newtons es: {empuje: .2f}")