from datetime import datetime  

# Función para calcular la inversión  
def calcular_inversion(monto_inicial, fecha_inicio, rendimiento_mensual):  
    fecha_actual = datetime.now()  
    meses_transcurridos = (fecha_actual.year - fecha_inicio.year) * 12 + (fecha_actual.month - fecha_inicio.month)  
    
    # Cálculo del valor futuro de la inversión  
    valor_futuro = monto_inicial * (1 + rendimiento_mensual / 100) ** meses_transcurridos  
    return valor_futuro  

while True:  
    # Solicitar datos al usuario  
    monto = float(input("Ingresa el monto de la inversión: "))  
    fecha_input = input("Ingresa la fecha de inicio (YYYY-MM-DD): ")  
    rendimiento_mensual = float(input("Ingresa el rendimiento mensual en porcentaje: "))  

    # Convertir la fecha ingresada a un objeto datetime  
    fecha_inicio = datetime.strptime(fecha_input, "%Y-%m-%d")  

    # Calcular el valor de la inversión  
    valor_final = calcular_inversion(monto, fecha_inicio, rendimiento_mensual)  

    # Mostrar el resultado  
    print(f"El valor de la inversión al día de hoy es: {valor_final:.2f}")  

    # Preguntar si desea realizar otro cálculo  
    respuesta = input("¿Quieres hacer otro cálculo? (si/no): ").strip().lower()  
    
    if respuesta != 'si':  
        print("Va, hasta luego")  
        break  
