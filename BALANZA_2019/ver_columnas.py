import pandas as pd

# Cargar el archivo de Excel
file_path = "BANCOS 2025.xlsx"
df = pd.read_excel(file_path, sheet_name="MXN")  # Ajusta el nombre de la hoja si es necesario

# Imprimir nombres de las columnas
print(df.columns.tolist())
