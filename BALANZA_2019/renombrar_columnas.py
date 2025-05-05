# Renombrar columnas si es necesario
df = df.rename(columns={'CLAVE': 'Cuenta', 'CARGO': 'Débito', 'ABONO': 'Crédito'})

# Agrupar por cuenta y sumar débitos y créditos
trial_balance = df.groupby(['Cuenta'])[['Débito', 'Crédito']].sum().reset_index()
