Option Explicit

Dim CATIA, doc, prod
Dim measure5, measure6
Dim finalValue

' Conectar a CATIA (instancia existente)
On Error Resume Next
Set CATIA = GetObject(, "CATIA.Application")
If CATIA Is Nothing Then
    WScript.Echo "CATIA no está ejecutándose."
    WScript.Quit 1
End If
On Error GoTo 0

Set doc = CATIA.ActiveDocument
If doc Is Nothing Then
    WScript.Echo "No hay documento activo."
    WScript.Quit 1
End If

' Intentar leer medidas desde la colección global (sin tipo)
measure5 = Null
measure6 = Null

On Error Resume Next
Dim measCol
Set measCol = doc.Measurements
If Not measCol Is Nothing Then
    measure5 = GetMeasurementValue(measCol, "MeasureBetween.5")
    measure6 = GetMeasurementValue(measCol, "MeasureBetween.6")
End If
On Error GoTo 0

' Si no se encuentran, intentar en el primer nivel de componentes
If Not IsNumeric(measure5) Or Not IsNumeric(measure6) Then
    Set prod = doc.Product
    If Not prod Is Nothing Then
        Dim comp
        For Each comp In prod.Products
            Dim cMeas
            On Error Resume Next
            Set cMeas = comp.Measurements
            If Not cMeas Is Nothing Then
                Dim mVal
                mVal = GetMeasurementValue(cMeas, "MeasureBetween.5")
                If IsNumeric(mVal) Then measure5 = CDbl(mVal)
                mVal = GetMeasurementValue(cMeas, "MeasureBetween.6")
                If IsNumeric(mVal) Then measure6 = CDbl(mVal)
            End If
            On Error GoTo 0
            If IsNumeric(measure5) And IsNumeric(measure6) Then Exit For
        Next
    End If
End If

If Not IsNumeric(measure5) Or Not IsNumeric(measure6) Then
    WScript.Echo "No se pudieron obtener MeasureBetween.5 y MeasureBetween.6."
    WScript.Quit 1
End If

' Cálculos
finalValue = (((measure5 - 270) * 0.7539) * measure6) / 250

' Mostrar resultado
WScript.Echo "Valor final (R): " & finalValue

' Función auxiliar
Function GetMeasurementValue(measCol, name)
    Dim m
    On Error Resume Next
    Set m = measCol.Item(name)
    If Not m Is Nothing Then
        GetMeasurementValue = m.Value
    Else
        GetMeasurementValue = Null
    End If
    On Error GoTo 0
End Function