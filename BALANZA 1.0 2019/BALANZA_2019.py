import pandas as pd

try:
    # Cargar el archivo de Excel
    file_path = "BANCOS 2025.xlsx"  # Ajusta el nombre de tu archivo
    df = pd.read_excel(file_path, sheet_name="MXN")

    # Limpiar nombres de columnas (ya no es necesario, son correctos)
    #df.columns = df.columns.str.strip()

    # Renombrar columnas (opcional, si prefieres nombres en inglés)
    #df = df.rename(columns={'CLAVE': 'Cuenta', 'CARGO': 'Débito', 'ABONO': 'Crédito'})

    # Convertir Débito y Crédito a valores numéricos
    df['Débito'] = pd.to_numeric(df['Débito'], errors='coerce').fillna(0)
    df['Crédito'] = pd.to_numeric(df['Crédito'], errors='coerce').fillna(0)

    # Agrupar por Cuenta y Nombre de cuenta (si quieres agrupar por ambas)
    trial_balance = df.groupby(['Cuenta', 'Nombre de cuenta'])[['Débito', 'Crédito']].sum().reset_index()

    # Si quieres agrupar solo por Cuenta, usa esta línea en lugar de la anterior:
    # trial_balance = df.groupby(['Cuenta'])[['Débito', 'Crédito']].sum().reset_index()

    # Calcular el saldo
    trial_balance['Saldo'] = trial_balance['Débito'] - trial_balance['Crédito']

    # Mostrar resultado
    print(trial_balance)

    # Exportar a Excel
    trial_balance.to_excel("Balanza_Comprobacion_2025.xlsx", index=False)

except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{file_path}'.")
except KeyError as e:
    print(f"Error: La columna '{e}' no se encontró en el archivo.")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")