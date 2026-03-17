Option Explicit

Dim CATIA, doc
Dim measure_LARGO, measure_PALANCA

' 1. Conexión a CATIA
Set CATIA = GetObject(, "CATIA.Application")
If CATIA Is Nothing Then
    WScript.Echo "CATIA no está ejecutándose. Asegúrese de que CATIA V5 esté abierto."
    WScript.Quit 1
End If

Set doc = CATIA.ActiveDocument
If doc Is Nothing Then
    WScript.Echo "No hay documento activo."
    WScript.Quit 1
End If

' Diagnóstico: Confirmar el documento leído
WScript.Echo "Documento activo: " & doc.Name & " (Tipo: " & doc.Product.Name & ")"

measure_LARGO = Null
measure_PALANCA = Null

' Intentar forzar la actualización para asegurar que las medidas estén frescas
On Error Resume Next
doc.Update ' Forzar actualización
On Error GoTo 0

' **Nombres de las medidas actualizados**
Const MEASURE_NAME_LARGO = "LARGO"
Const MEASURE_NAME_PALANCA = "PALANCA"

' -------------------------------------------------------------------
' ## Intento 1: Buscar en el Documento Activo Global (CATProduct Principal)
' -------------------------------------------------------------------
WScript.Echo "--- Buscando en el documento principal ---"

' Se intenta buscar en las colecciones del documento (si es un Product, o si es un Part)
measure_LARGO = GetMeasurementValue(doc, MEASURE_NAME_LARGO)
measure_PALANCA = GetMeasurementValue(doc, MEASURE_NAME_PALANCA)

WScript.Echo "Lecturas global -> LARGO=" & SafeCStr(measure_LARGO) & " PALANCA=" & SafeCStr(measure_PALANCA)

' -------------------------------------------------------------------
' ## Intento 2: Buscar en los Componentes (Parts o Sub-Products)
' -------------------------------------------------------------------
If Not IsNumeric(measure_LARGO) Or Not IsNumeric(measure_PALANCA) Then
    WScript.Echo "--- Buscando en los componentes anidados ---"
    
    Dim prod, comp
    Set prod = doc.Product ' Objeto Product del documento activo
    
    If Not prod Is Nothing Then
        For Each comp In prod.Products ' Itera a través de todos los componentes
            Dim compContainer
            On Error Resume Next
            ' ACCESO CLAVE: Intentar obtener el objeto Part del componente (más probable que contenga medidas)
            Set compContainer = comp.ReferenceProduct.Parent.Part 
            
            ' Si no es un Part, intentar obtener el Product (si es un sub-ensamblaje)
            If compContainer Is Nothing Then
                Set compContainer = comp.ReferenceProduct.Parent.Product
            End If
            
            On Error GoTo 0
            
            If Not compContainer Is Nothing Then
                WScript.Echo "  -> Buscando en: " & comp.Name

                Dim v2
                v2 = GetMeasurementValue(compContainer, MEASURE_NAME_LARGO)
                If IsNumeric(v2) Then measure_LARGO = CDbl(v2)
                v2 = GetMeasurementValue(compContainer, MEASURE_NAME_PALANCA)
                If IsNumeric(v2) Then measure_PALANCA = CDbl(v2)
               
                If IsNumeric(measure_LARGO) And IsNumeric(measure_PALANCA) Then 
                    WScript.Echo "  -> Medidas encontradas en: " & comp.Name
                    Exit For
                End If
            End If
        Next
    End If
End If

WScript.Echo "Lecturas finales -> LARGO=" & SafeCStr(measure_LARGO) & " PALANCA=" & SafeCstr(measure_PALANCA)

' -------------------------------------------------------------------
' ## Validación y Cálculo Final
' -------------------------------------------------------------------

If Not IsNumeric(measure_LARGO) Or Not IsNumeric(measure_PALANCA) Then
    WScript.Echo "FALLA: No se pudieron obtener ambas medidas numéricas. Revise la ubicación de las medidas en el árbol."
    WScript.Quit 1
End If

Dim finalValue
' Realizar la operación.
finalValue = (((CDbl(measure_LARGO) - 270) * 0.7539) * CDbl(measure_PALANCA)) / 250
WScript.Echo "---"
WScript.Echo "Cálculo final exitoso."
WScript.Echo "Valor final (R) = " & finalValue


' -------------------------------------------------------------------
' ## Funciones de Utilidad
' -------------------------------------------------------------------

Function GetMeasurementValue(objContainer, name)
    ' Devuelve el valor numérico (Double) o la cadena "NO ENCONTRADA"
    Dim m, measCol
    GetMeasurementValue = "NO ENCONTRADA" 
    
    On Error Resume Next
    
    ' Se asume que las medidas están en la colección .Measurements del objeto Part/Product.
    Set measCol = objContainer.Measurements 
    If Not measCol Is Nothing Then
        Set m = measCol.Item(name)
        If Not m Is Nothing Then
            GetMeasurementValue = m.Value ' <-- Devuelve el valor numérico
            Exit Function
        End If
    End If
    
    On Error GoTo 0
End Function

Function SafeCStr(v)
    ' Maneja Null y la cadena "NO ENCONTRADA" de forma segura.
    If IsNull(v) Or v = "NO ENCONTRADA" Then
        SafeCStr = "NO ENCONTRADA"
    Else
        SafeCStr = CStr(v)
    End If
End Function