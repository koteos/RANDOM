import pandas as pd

# Paso 2: Cargar el archivo
xls = pd.ExcelFile("BANCOS 2025.xlsx")
print("Hojas disponibles:", xls.sheet_names)
# Ajusta el nombre de la hoja según corresponda
df = pd.read_excel("BANCOS 2025.xlsx", sheet_name=xls.sheet_names[0])

# Paso 3: Inspeccionar datos
print(df.head())

# Paso 4: Agrupar por Cuenta y Nombre de Cuenta
trial_balance = df.groupby(['Cuenta', 'Nombre de Cuenta'])[['Débito', 'Crédito']].sum().reset_index()

# Paso 5: Calcular el saldo
trial_balance['Saldo'] = trial_balance['Débito'] - trial_balance['Crédito']

# Paso 6: Mostrar resultado
print(trial_balance)

# Paso 7: Exportar a Excel (opcional)
trial_balance.to_excel("Balanza_Comprobacion_2025.xlsx", index=False)