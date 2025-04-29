import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# === CONFIGURACION INICIAL ===
# Ingresos proyectados: lista de diccionarios con fecha de facturacion, monto y dias de pago
proyecciones = [
    {"cliente": "HEINEKEN", "fecha_factura": "2025-05-10", "monto": 250000, "dias_pago": 60},
    {"cliente": "BIMBO", "fecha_factura": "2025-05-15", "monto": 180000, "dias_pago": 45},
    {"cliente": "COPPEL", "fecha_factura": "2025-06-05", "monto": 220000, "dias_pago": 60},
    {"cliente": "LACOMER", "fecha_factura": "2025-06-20", "monto": 150000, "dias_pago": 30},
    {"cliente": "AUDI", "fecha_factura": "2025-07-01", "monto": 300000, "dias_pago": 90},
]

# Gastos mensuales fijos (puedes agregar más)
gastos_fijos = [
    {"concepto": "Nómina", "monto": 320000},
    {"concepto": "Renta", "monto": 30000},
    {"concepto": "Servicios", "monto": 10000},
    {"concepto": "Otros", "monto": 10000},
]

# Fecha de inicio de simulación y meses a proyectar
inicio = datetime(2025, 5, 1)
meses = 6

# === PROCESAMIENTO ===
# Crear DataFrame base de meses
fechas = pd.date_range(inicio, periods=meses, freq='MS')
df = pd.DataFrame({"Fecha": fechas})
df["Ingresos"] = 0

# Calcular ingresos por mes
for p in proyecciones:
    fecha_pago = pd.to_datetime(p["fecha_factura"]) + timedelta(days=p["dias_pago"])
    mes_pago = datetime(fecha_pago.year, fecha_pago.month, 1)
    df.loc[df["Fecha"] == mes_pago, "Ingresos"] += p["monto"]

# Calcular egresos por mes
df["Egresos"] = sum(g["monto"] for g in gastos_fijos)

# Calcular flujo neto y acumulado
df["Flujo Neto"] = df["Ingresos"] - df["Egresos"]
df["Flujo Acumulado"] = df["Flujo Neto"].cumsum()

# === GRAFICADO ===
import matplotlib.pyplot as plt
print(plt.style.available)

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(df["Fecha"], df["Ingresos"], width=20, label="Ingresos", color="green")
ax.bar(df["Fecha"], df["Egresos"] * -1, width=20, label="Egresos", color="red")
ax.plot(df["Fecha"], df["Flujo Acumulado"], label="Flujo Acumulado", marker='o', color="blue")

ax.set_title("Simulación de Flujo de Efectivo")
ax.set_ylabel("Monto ($MXN)")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()
