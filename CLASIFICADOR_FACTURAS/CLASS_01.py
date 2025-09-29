import pdfplumber
import pandas as pd
import os
import re

# Ruta a la carpeta donde están los PDFs
carpeta_pdfs = r"F:\FAC\ALL"
ruta_salida_excel = r"F:\FAC\resumen_facturas.xlsx"

resultados = []

def extraer_datos_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto_extraido = pagina.extract_text()
            if texto_extraido:
                texto += texto_extraido + "\n"

    nombre_archivo = os.path.basename(pdf_path)

    subtotal_match = re.search(r"Sub[\s\-]*Total\s*[:\$]*\s*\$?\s*([\d,]+\.\d{2})", texto, re.IGNORECASE)
    total_match = re.search(r"Total\s*[:\$]*\s*\$?\s*([\d,]+\.\d{2})", texto, re.IGNORECASE)
    iva_match = re.search(r"IVA.*?\s*[:\$]*\s*\$?\s*([\d,]+\.\d{2})", texto, re.IGNORECASE)

    rfc_emisor = re.search(r"RFC\s*:\s*([A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3})", texto)
    rfc_receptor = re.findall(r"RFC\s*:\s*([A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3})", texto)

    subtotal = float(subtotal_match.group(1).replace(",", "")) if subtotal_match else None
    total = float(total_match.group(1).replace(",", "")) if total_match else None
    iva = float(iva_match.group(1).replace(",", "")) if iva_match else None

    emisor = rfc_emisor.group(1) if rfc_emisor else ""
    receptor = rfc_receptor[1] if len(rfc_receptor) > 1 else ""

    fecha_match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", texto)
    fecha = fecha_match.group(0) if fecha_match else ""

    return {
        "archivo": nombre_archivo,
        "rfc_emisor": emisor,
        "rfc_receptor": receptor,
        "fecha": fecha,
        "subtotal_sin_iva": subtotal,
        "iva": iva,
        "total_con_iva": total
    }

# Procesar todos los PDFs en la carpeta
for archivo in os.listdir(carpeta_pdfs):
    if archivo.lower().endswith(".pdf"):
        ruta_completa = os.path.join(carpeta_pdfs, archivo)
        try:
            datos = extraer_datos_pdf(ruta_completa)
            resultados.append(datos)
            print(f"✅ Procesado: {archivo}")
        except Exception as e:
            print(f"⚠️ Error procesando {archivo}: {e}")

# Crear DataFrame
df = pd.DataFrame(resultados)

# Crear hoja resumen con totales
resumen = pd.DataFrame({
    "concepto": ["Total subtotal sin IVA", "Total IVA", "Total con IVA"],
    "monto": [
        df["subtotal_sin_iva"].sum(),
        df["iva"].sum(),
        df["total_con_iva"].sum()
    ]
})

print("📊 Total de facturas procesadas:", len(resultados))

# Guardar a Excel con dos hojas en F:\FAC\
with pd.ExcelWriter(ruta_salida_excel, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Facturas", index=False)
    resumen.to_excel(writer, sheet_name="Totales", index=False)

print(f"✅ ¡Listo! Archivo guardado en: {ruta_salida_excel}")
