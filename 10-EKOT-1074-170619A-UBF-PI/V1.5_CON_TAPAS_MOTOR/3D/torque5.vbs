Option Explicit

Dim CATIA, doc
Dim measure5, measure6

Set CATIA = GetObject(, "CATIA.Application")
If CATIA Is Nothing Then
    WScript.Echo "CATIA no está ejecutándose."
    WScript.Quit 1
End If

Set doc = CATIA.ActiveDocument
If doc Is Nothing Then
    WScript.Echo "No hay documento activo."
    WScript.Quit 1
End If

measure5 = Null
measure6 = Null

' -------------------------------------------------------------------
' ## Intento 1: Buscar en el Documento Activo Global (Product o Part)
' -------------------------------------------------------------------
On Error Resume Next
Dim measCol
' Si es un CATPart, es doc.Part.Measurements. Si es un CATProduct es doc.Measurements
Set measCol = doc.Measurements 
If Not measCol Is Nothing Then
    Dim v
    v = GetMeasurementValue(measCol, "MeasureBetween.5")
    If IsNumeric(v) Then measure5 = CDbl(v)
    v = GetMeasurementValue(measCol, "MeasureBetween.6")
    If IsNumeric(v) Then measure6 = CDbl(v)
End If
On Error GoTo 0

WScript.Echo "Lecturas global -> measure5=" & SafeCStr(measure5) & " measure6=" & SafeCStr(measure6)

' -------------------------------------------------------------------
' ## Intento 2: Buscar en el primer nivel de Componentes (Assembly)
' -------------------------------------------------------------------
If Not IsNumeric(measure5) Or Not IsNumeric(measure6) Then
    Dim prod, comp, v2
    Set prod = doc.Product
    
    If Not prod Is Nothing Then
        For Each comp In prod.Products
            Dim compPart
            On Error Resume Next
            ' Obtener la Part (o Sub-Product) donde realmente está la medida
            Set compPart = comp.ReferenceProduct.Parent.Part
            On Error GoTo 0

            If Not compPart Is Nothing Then
                Dim cMeas
                On Error Resume Next
                Set cMeas = compPart.Measurements
                If Not cMeas Is Nothing Then
                    v2 = GetMeasurementValue(cMeas, "MeasureBetween.5")
                    If IsNumeric(v2) Then measure5 = CDbl(v2)
                    v2 = GetMeasurementValue(cMeas, "MeasureBetween.6")
                    If IsNumeric(v2) Then measure6 = CDbl(v2)
                End If
                On Error GoTo 0
               
                If IsNumeric(measure5) And IsNumeric(measure6) Then Exit For
            End If
        Next
    End If
End If

WScript.Echo "Lecturas finales -> measure5=" & SafeCStr(measure5) & " measure6=" & SafeCStr(measure6)

If Not IsNumeric(measure5) Or Not IsNumeric(measure6) Then
    WScript.Echo "No se pudieron obtener medidas numéricas."
    WScript.Quit 1
End If

' -------------------------------------------------------------------
' ## Cálculo Final
' -------------------------------------------------------------------
Dim finalValue
finalValue = (((CDbl(measure5) - 270) * 0.7539) * CDbl(measure6)) / 250
WScript.Echo "Valor final (R) = " & finalValue

' -------------------------------------------------------------------
' ## Funciones de Utilidad
' -------------------------------------------------------------------

Function GetMeasurementValue(measCol, name)
    Dim m
    On Error Resume Next
    Set m = measCol.Item(name)
    
    If Not m Is Nothing Then
        ' El objeto fue encontrado: devolvemos su valor.
        ' Esto debería ser el número real de la distancia.
        GetMeasurementValue = m.Value
    Else
        ' El objeto NO fue encontrado: devolvemos una cadena para saberlo.
        ' ¡Esto nos dirá que el nombre estaba mal o la colección incorrecta!
        GetMeasurementValue = "NO ENCONTRADA"
    End If
    
    On Error GoTo 0
End Function

Function SafeCStr(v)
    ' Soluciona el error 800A005E 'Uso no válido de Null: CStr'
    If IsNull(v) Then
        SafeCStr = "Null"
    Else
        SafeCStr = CStr(v)
    End If
End Function