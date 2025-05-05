import pandas as pd

# Valores base para los costos mensuales adicionales
maintenance_cost = 500       # Mantenimiento mensual
insurance_cost = 300         # Seguro y garantías mensual
admin_cost = 200             # Administración y atención al cliente mensual
profit_margin = 0.30         # 30% de utilidad

# Crear un DataFrame de ejemplo para mostrar la estructura
data = {
    "Descripción": [
        "Costo del equipo (entrada del usuario)",
        "Plazo del arrendamiento (meses, entrada del usuario)",
        "Mantenimiento mensual",
        "Seguro y garantías mensual",
        "Administración y atención al cliente mensual",
        "Costo mensual base sin utilidad",
        "Renta mensual con utilidad"
    ],
    "Valor": [
        "=B2",                 # Costo del equipo
        "=B3",                 # Plazo en meses
        maintenance_cost,
        insurance_cost,
        admin_cost,
        "=B2/B3 + B4 + B5 + B6",  # Base mensual sin utilidad
        "=(B2/B3 + B4 + B5 + B6) * (1 + 0.30)"  # Con utilidad
    ]
}

df = pd.DataFrame(data)

# Guardar como archivo Excel
file_path = "/mnt/data/RaaS_rent_calculator.xlsx"
df.to_excel(file_path, index=False)

file_path
